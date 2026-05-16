import multiprocessing
import signal
import itertools

import cv2
import numpy as np

from .constants import Position, MatchResults, Region, PARALLEL_MAX_WORKERS, LEVEL_START_END_DETECTION_THR, TEMPLATE_LEVEL_START_PATH


def find_viewport(frames_generator, black_value_thr = 5):
    # Estimate the drawable screen portion from the frames.
    viewport_start = Position(row = +float("inf"), col = +float("inf"))
    viewport_stop  = Position(row = -float("inf"), col = -float("inf"))

    for frame in frames_generator:
        # Get the non-black pixels and use them to calculate drawable height and width.
        mask = ~cv2.inRange(frame, (0, 0, 0), (black_value_thr, black_value_thr, black_value_thr))
        rows, cols = mask.nonzero()
        if rows.size == 0:
            continue

        viewport_start = Position(row = min(viewport_start.row, min(rows)),
                                  col = min(viewport_start.col, min(cols)))
        viewport_stop  = Position(row = max(viewport_stop.row , max(rows) + 1),
                                  col = max(viewport_stop.col , max(cols) + 1))

    return Region(start = viewport_start, stop = viewport_stop)


def find_scale_and_maze_region(frames_generator, scale_pixels_trial_range = 20, successful_match_thr = LEVEL_START_END_DETECTION_THR):
    # Load template_level_start. Must not have any alpha channel because if it does template match considers transparency in match.
    template_level_start = load_image(TEMPLATE_LEVEL_START_PATH, transparency = False)
    template_height, template_width, _ = template_level_start.shape

    # Confirm frames_generator has an active viewport, since otherwise we can't easily know the size of the approximate size of the template in the frames.
    viewport = frames_generator.viewport
    if viewport is None:
        raise RuntimeError(f"Provided frames_generator does not have an active viewport.")

    # In theory, the image in template_level_start should span the whole width of the drawable screen.
    theoretical_template_width  = viewport.width
    theoretical_template_height = int((theoretical_template_width / template_width) * template_height)

    # Due to video compression artefacts, our estimate may not be precise enough. Hence we instead try a few values around it.
    scaled_templates = []
    for width in range(max(theoretical_template_width - scale_pixels_trial_range, 1),
                       min(theoretical_template_width + scale_pixels_trial_range, viewport.width + 1)):
        for height in range(max(theoretical_template_height - scale_pixels_trial_range, 1),
                            min(theoretical_template_height + scale_pixels_trial_range, viewport.height + 1)):
            scaled_templates.append(resize_image(template_level_start, width = width, height = height))
    results = match_template_whole_video(frames_generator, scaled_templates)
    del theoretical_template_width, theoretical_template_height, width, height

    # Find the best results and calculate the scaling along each axis to achieve it.
    results = [{"score": res.score, "scale_idx": scale_idx, "position": res.pos} for frame_results in results for scale_idx, res in enumerate(frame_results)]
    best_result = min(results, key = lambda e: e["score"])
    best_scaled_height, best_scaled_width, _ = scaled_templates[best_result["scale_idx"]].shape
    scale_height = best_scaled_height / template_height
    scale_width  = best_scaled_width  / template_width

    # As a bonus, we also get the position of the maze inside our viewport. Convert it into frame position and store it for later.
    maze_region = Region(start  = best_result["position"] + viewport.start,
                         height = best_scaled_height,
                         width  = best_scaled_width)

    # Sanity check.
    if best_result["score"] > successful_match_thr:
        raise RuntimeError(f"Could not find scale of frames_generator using template provided. Best score was {best_result["score"]} which is lower than required {successful_match_thr}.")

    return scale_height, scale_width, maze_region


def match_template_whole_video(frames_generator, sprites, crop_frame_callback = None, **video_iterator_kwargs):
    if not isinstance(sprites, (tuple, list)):
        raise RuntimeError(f"Expected sprites argument to be a list or tuple of images. Got {type(sprites)}")

    sprites = [s    for s in sprites]
    masks   = [None for _ in sprites]
    for idx, s in enumerate(sprites):
        check_image_shape(s, n_channels = (3, 4))
        if s.shape[-1] == 4:
            sprites[idx] = s[:, :, :-1]
            masks  [idx] = s[:, :, -1]
    del idx, s

    try:
        iterator = zip(frames_generator,
                       itertools.repeat(sprites),
                       itertools.repeat(masks),
                       itertools.repeat(crop_frame_callback))

        with multiprocessing.Pool(PARALLEL_MAX_WORKERS, init_worker) as pool:
            results = list(pool.imap(analyse_frame, iterator))

    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
        raise

    return results


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def check_image_shape(image, n_channels, n_dims = 3):
    if not isinstance(n_channels, (tuple, list)):
        n_channels = [n_channels]

    if image.ndim != n_dims or image.shape[-1] not in n_channels:
        raise RuntimeError(f"Expected image with {n_dims} dimentions, with last one encoding one of {n_channels} channels. Instead got shape: {image.shape}")


def analyse_frame(args):
    frame, sprites, masks, crop_frame_callback = args

    if not isinstance(sprites, (list, tuple)) or not isinstance(masks, (list, tuple)):
        raise RuntimeError(f"Arguments sprites and masks should both be either list or tuple. Got {type(sprites)} and {type(masks)} respectively.")
    if len(sprites) != len(masks):
        raise RuntimeError(f"The number of sprites and masks do not match. Got {len(sprites)} and {len(masks)} respectively.")

    crop_position = Position(row = 0, col = 0)
    if crop_frame_callback is not None:
        if not callable(crop_frame_callback):
            raise RuntimeError("argument 'crop_frame_callback' must be callable.")

        frame, crop_position = crop_frame_callback(frame)
        if frame is None:
            return [MatchResults.NO_MATCH for _ in zip(sprites, masks)]

        if not isinstance(crop_position, Position):
            raise RuntimeError("argument 'crop_frame_callback' needs to return cropped frame and an instance of class Position.")

    check_image_shape(frame, n_channels = 3)

    results = []
    for sprite, mask in zip(sprites, masks):
        values = cv2.matchTemplate(frame, sprite, method = cv2.TM_SQDIFF, mask = mask)

        if np.isnan(values).any():
            raise RuntimeError("Some values resulting from cv2.matchTemplate are null...")

        min_val, _, (col, row), _ = cv2.minMaxLoc(values)

        denominator = np.sum(mask != 0, axis = None) if mask is not None else sprite.shape[0] * sprite.shape[1]
        min_val = np.sqrt(min_val / denominator)

        results.append(MatchResults(Position(row, col) + crop_position, min_val))

    return results


def load_image(path, transparency, resize_kwargs = None):
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED if transparency else cv2.IMREAD_COLOR)
    _, _, n_channels = image.shape

    if transparency and n_channels != 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        _, _, n_channels = image.shape

    if resize_kwargs is not None:
        image = resize_image(image, **resize_kwargs)

    # Sanity check.
    expected_n_channels = 4 if transparency else 3
    if n_channels != expected_n_channels:
        raise RuntimeError(f"Programming error caused image to be loaded with {n_channels} instead of {expected_n_channels} with transparency={transparency}")

    return image


def resize_image(image, height = None, width = None, scale_width = None, scale_height = None):
    shrinking = None
    use_scale = None
    if height is None and width is None and scale_width is not None and scale_height is not None:
        shrinking = scale_width <= 1
        use_scale = True
    elif height is not None and width is not None and scale_width is None and scale_height is None:
        shrinking = width <= image.shape[1]
        use_scale = False
    else:
        raise ValueError("this function expects either 'width' and 'height' or 'scale_width' and 'scale_height' to be provided at the same time")

    return cv2.resize(image,
                      None if use_scale else (width, height),
                      fx = scale_width,
                      fy = scale_height,
                      interpolation = cv2.INTER_AREA if shrinking else cv2.INTER_CUBIC)
import multiprocessing
import signal
import itertools
from dataclasses import dataclass

import cv2
from tqdm import tqdm
import numpy as np

from constants import VIDEOS_PATHS, TEMPLATE_LEVEL_START_PATH, TEMPLATE_LEVEL_END_PATH, PARALLEL_MAX_WORKERS, LEVEL_SEARCH_FRAMES_STEP


@dataclass(slots = True, frozen = True)
class Position:
    row: int
    col: int

    def __add__(self, other):
        if not isinstance(other, Position):
            raise ValueError(f"argument 'other' must be of type Position. Got {type(other)}")
        return Position(row = self.row + other.row, col = self.col + other.col)
    

@dataclass(slots = True, frozen = True)
class MatchResults:
    pos: Position
    score: float


@dataclass(slots = True, frozen = True)
class Region:
    start: Position
    stop: Position
    height = property(lambda self: self.stop.row - self.start.row)
    width  = property(lambda self: self.stop.col - self.start.col)

    def __init__(self, start, stop = None, height = None, width = None):
        if not isinstance(start, Position):
            raise ValueError(f"argument 'start' must be of type Position. Got {type(start)}")
        if stop is None:
            if not isinstance(height, int) or not isinstance(width, int):
                raise ValueError(f"when argument 'stop' is not provided, both 'width' and 'height' must be provided and must be integers. Got {type(width)} and {type(height)} respectively.")
            stop = Position(row = start.row + height, col = start.col + width)
        else:
            if height is not None or width is not None:
                raise ValueError(f"when argument 'stop' is provided, both 'width' and 'height' must not be provided")
        
        if start.row > stop.row or start.col > stop.col:
            raise ValueError(f"start must have row and col <= to stop. Got start: {start} and stop {stop}")

        object.__setattr__(self, "start", start)
        object.__setattr__(self, "stop" , stop)





def __make_all_sprites():
    # ------------------------------------------------------------------------
    # Coped from game constants.
    # ------------------------------------------------------------------------

    from collections import namedtuple

    # Path of the atlas image.
    GRAPHICS_ATLAS_PATH = "./assets/images/atlas.png"

    # Named tuple used to store information on the regions composing the atlas.
    _AtlasRegion = namedtuple("AtlasRegion", ["reg_x_left", "reg_y_bottom", "reg_width", "reg_height", "elem_width", "elem_height"])

    # Coordinates in pixels of each region composing the atlas.
    # Regions are zones in the atlas where the sub-elements have uniform sizes and are grouped for easy coordinate calculation.
    _GRAPHICS_ATLAS_REGION_TEXT   = _AtlasRegion(0  , 0  , 128, 256, 8 , 8 )
    _GRAPHICS_ATLAS_REGION_MAZE   = _AtlasRegion(128, 0  , 672, 248, 8 , 8 )
    _GRAPHICS_ATLAS_REGION_SCORES = _AtlasRegion(800, 0  , 96 , 72 , 24, 24)
    _GRAPHICS_ATLAS_REGION_GHOSTS = _AtlasRegion(0  , 256, 192, 64 , 16, 16)
    _GRAPHICS_ATLAS_REGION_PACMAN = _AtlasRegion(192, 256, 224, 64 , 16, 16)
    _GRAPHICS_ATLAS_REGION_FRUITS = _AtlasRegion(416, 256, 144, 16 , 16, 16)

    # ------------------------------------------------------------------------


    im = cv2.imread(GRAPHICS_ATLAS_PATH, cv2.IMREAD_UNCHANGED)

    sprites = []
    for region in GRAPHICS_ATLAS_ALL_REGIONS:
        left   = region.reg_x_left
        right  = left + region.reg_width
        bottom = im.shape[0] - region.reg_y_bottom
        top    = bottom - region.reg_height

        for row in range(top, bottom, region.elem_height):
            for col in range(left, right, region.elem_width):
                sprites.append(im[row:row+region.elem_height, col:col+region.elem_width])

    # Remove repetitions.
    seen = set()
    idx_to_remove = []
    for idx, sprite in enumerate(sprites):
        hashable = sprite.tobytes()
        if hashable in seen:
            idx_to_remove.append(idx)
        else:
            seen.add(hashable)
    sprites = [s for idx, s in enumerate(sprites) if idx not in idx_to_remove]

    return sprites





def video_iterator(video_path, frames_start = 0, frames_step = 1, frames_number = None, viewport = None):
    stream = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
    n_frames_video = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))

    frames_end = n_frames_video if frames_number is None else frames_start + frames_step * frames_number
    frames_to_yield = range(frames_start, frames_end, frames_step)

    current_frame = -1
    
    with tqdm(total = len(frames_to_yield), ascii = True, leave = False) as pbar:
        while True:
            current_frame += 1

            if current_frame in frames_to_yield:
                grabbed, frame = stream.read()
            else:
                grabbed = stream.grab()

            if not grabbed:
                break
            elif current_frame >= frames_end:
                break
            elif current_frame not in frames_to_yield:
                continue
            
            pbar.update()
            if viewport is not None:
                frame = frame[viewport.start.row:viewport.stop.row, viewport.start.col:viewport.stop.col]
            yield frame
        
    stream.release()


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def check_and_make_template_mask(frame, sprite):
    if frame.ndim != 3 or frame.shape[-1] != 3:
        raise RuntimeError(f"Template matching expects frame to have 3 dimentions, with last one encoding 3 channels. Instead got shape: {frame.shape}")
    if sprite.ndim != 3 or frame.shape[-1] not in (3, 4):
        raise RuntimeError(f"Template matching expects sprite to have 3 dimentions, with last one encoding 3 or 4 channels. Instead got shape: {sprite.shape}")
    
    mask = None
    if sprite.shape[-1] == 4:
        mask = sprite[:, :, -1]
        sprite = sprite[:, :, :-1]

    return sprite, mask


def check_image_shape(image, n_channels, n_dims = 3):
    if not isinstance(n_channels, (tuple, list)):
        n_channels = [n_channels]

    if image.ndim != n_dims or image.shape[-1] not in n_channels:
        raise RuntimeError(f"Expected image with {n_dims} dimentions, with last one encoding one of {n_channels} channels. Instead got shape: {image.shape}")



def match_template_whole_video(video_path, sprites, **video_iterator_kwargs):
    if not isinstance(sprites, (tuple, list)):
        raise RuntimeError(f"Expected sprites argument to be a list or tuple of images. Got {type(sprites)}")
    
    sprites = [s    for s in sprites]
    masks   = [None for _ in sprites]
    for idx, s in enumerate(sprites):
        check_image_shape(s, n_channels = (3, 4))
        if s.shape[-1] == 4:
            sprites[idx] = s[:, :, :-1]
            masks  [idx] = s[:, :, -1]
    del s

    try:
        iterator = zip(video_iterator(video_path, **video_iterator_kwargs), 
                       itertools.repeat(sprites), 
                       itertools.repeat(masks))

        with multiprocessing.Pool(PARALLEL_MAX_WORKERS, init_worker) as pool:
            results = list(pool.imap(analyse_frame, iterator))

    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
        raise
    
    return results


def analyse_frame(args):
    frame, sprites, masks = args

    check_image_shape(frame, n_channels = 3)
    if not isinstance(sprites, (list, tuple)) or not isinstance(masks, (list, tuple)):
        raise RuntimeError(f"Arguments sprites and masks should both be either list or tuple. Got {type(sprites)} and {type(masks)} respectively.")
    if len(sprites) != len(masks):
        raise RuntimeError(f"The number of sprites and masks do not match. Got {len(sprites)} and {len(masks)} respectively.")

    results = []
    for sprite, mask in zip(sprites, masks):
        values = cv2.matchTemplate(frame, sprite, method = cv2.TM_SQDIFF, mask = mask)

        if np.isnan(values).any():
            raise RuntimeError("Some values resulting from matchTemplate are null...")

        min_val, _, (col, row), _ = cv2.minMaxLoc(values)

        denominator = np.sum(mask != 0, axis = None) if mask is not None else sprite.shape[0] * sprite.shape[1]
        min_val = np.sqrt(min_val / denominator)

        results.append(MatchResults(Position(row, col), min_val))

    return results


def find_viewport(video_path, frames_to_search = 200, frames_step = 30, black_value_thr = 5):
    # Estimate the drawable screen portion from the video.
    viewport_start = Position(row = +float("inf"), col = +float("inf"))
    viewport_stop  = Position(row = -float("inf"), col = -float("inf"))
    
    for frame in video_iterator(video_path, frames_step = frames_step, frames_number = frames_to_search):
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


def find_scale_and_maze_region(video_path, template_level_start_path, viewport, frames_to_search = 75, frames_step = 15, scale_pixels_trial_range = 20, successful_match_thr = 50):
    # Load template_level_start. Must not have any alpha channel because if it does template match considers transparency in match. 
    template_level_start = load_image(template_level_start_path, transparency = False)
    template_height, template_width, _ = template_level_start.shape
    
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
    results = match_template_whole_video(video_path, scaled_templates, viewport = viewport, frames_step = frames_step, frames_number = frames_to_search)
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
        raise RuntimeError(f"Could not find scale of video using template provided. Best score was {best_result["score"]}")

    return scale_height, scale_width, maze_region


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


def find_start_end_levels(video_path, template_level_start_path, template_level_end_path, maze_region, scale_height, scale_width):
    # Load templates for level start and level end. Must not have any alpha channel because if it does template match considers transparency in match. 
    template_level_start = load_image(template_level_start_path, transparency = False, resize_kwargs = {"scale_width": scale_width, "scale_height": scale_height})
    template_level_end   = load_image(template_level_end_path  , transparency = False, resize_kwargs = {"scale_width": scale_width, "scale_height": scale_height})

    # Search level start and end in each frame of the video.
    results = match_template_whole_video(video_path, [template_level_start, template_level_end], viewport = maze_region)

    import pickle
    pickle.dump(results, open(f"results_level_start_end.pkl", "wb"))

    import matplotlib.pyplot as plt
    plt.plot([r[0].score for r in results], label = 'start')
    plt.plot([r[1].score for r in results], label = 'end')
    plt.legend()
    plt.show()



        
    


if __name__ == "__main__":
    video_path = VIDEOS_PATHS[1]

    print("Finding viewport of video...")
    viewport = find_viewport(video_path)

    print("Finding scaling factors between video frames and templates...")
    scale_height, scale_width, maze_region = find_scale_and_maze_region(video_path, TEMPLATE_LEVEL_START_PATH, viewport)
    
    print("Detecting level starts scaling factors between video frames and templates...")
    find_start_end_levels(video_path, TEMPLATE_LEVEL_START_PATH, TEMPLATE_LEVEL_END_PATH, maze_region, scale_height, scale_width)
    




    print(viewport, scale_height, scale_width, maze_region)

    template_level_start = load_image(TEMPLATE_LEVEL_START_PATH, transparency = False, resize_kwargs = {"scale_width": scale_width, "scale_height": scale_height})
    for frame in video_iterator(video_path, frames_number = 500, frames_step = 10):
        offset = maze_region.start
        frame[offset.row:offset.row+template_level_start.shape[0], offset.col:offset.col+template_level_start.shape[1], :] = frame[offset.row:offset.row+template_level_start.shape[0], offset.col:offset.col+template_level_start.shape[1], :] * 0.5 + template_level_start * 0.5
        cv2.imshow("", frame)
        cv2.waitKey()

    quit()

    results = match_template_whole_video(video_path, [template_level_start], frames_step = LEVEL_SEARCH_FRAMES_STEP)
    
    import pickle
    pickle.dump(results, open(f"results_every_{LEVEL_SEARCH_FRAMES_STEP}.pkl", "wb"))

    import matplotlib.pyplot as plt
    plt.plot([r[0].SCORE for r in results])
    plt.show()
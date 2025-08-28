import multiprocessing
import signal
import itertools
from functools import partial

import cv2
from tqdm import tqdm
import numpy as np

from constants import Position, MatchResults, Region, VIDEOS_PATHS, TEMPLATE_LEVEL_START_PATH, TEMPLATE_LEVEL_END_PATH, PARALLEL_MAX_WORKERS, LEVEL_START_END_DETECTION_THR, TEMPLATE_PACMAN_PATH, TEMPLATE_PACMAN_LABEL_PER_ROW, TEMPLATE_PACMAN_ELEMENT_WIDTH, TEMPLATE_PACMAN_ELEMENT_HEIGHT, PACMAN_COLOR_RANGE_HSV, PACMAN_DETECTION_THR, PacmanStates



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


def video_get_fps(video_path):
    stream = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
    fps = float(stream.get(cv2.CAP_PROP_FPS))
    stream.release()

    if fps == 0.0:
        raise RuntimeError("unable to detect frames per second of video.")

    return fps


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



def match_template_whole_video(video_path, sprites, crop_frame_callback = None, **video_iterator_kwargs):
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
                       itertools.repeat(masks),
                       itertools.repeat(crop_frame_callback))

        with multiprocessing.Pool(PARALLEL_MAX_WORKERS, init_worker) as pool:
            results = list(pool.imap(analyse_frame, iterator))

    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
        raise
    
    return results


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


def find_scale_and_maze_region(video_path, template_level_start_path, viewport, frames_to_search = 75, frames_step = 15, scale_pixels_trial_range = 20, successful_match_thr = LEVEL_START_END_DETECTION_THR):
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


def find_start_end_levels(video_path, template_level_start_path, template_level_end_path, maze_region, scale_height, scale_width, level_start_end_detection_thr):
    # Load templates for level start and level end. Must not have any alpha channel because if it does template match considers transparency in match. 
    template_level_start = load_image(template_level_start_path, transparency = False, resize_kwargs = {"scale_width": scale_width, "scale_height": scale_height})
    template_level_end   = load_image(template_level_end_path  , transparency = False, resize_kwargs = {"scale_width": scale_width, "scale_height": scale_height})

    # Search level start and end in each frame of the video.
    results = match_template_whole_video(video_path, [template_level_start, template_level_end], viewport = maze_region)

    # Find detection edges to identify when level starts and ends.
    level_frame_ranges = []
    current_start = None

    for idx, (res_level_start, res_level_end) in enumerate(results):
        start_detected = res_level_start.score <= level_start_end_detection_thr
        end_detected   = res_level_end  .score <= level_start_end_detection_thr

        if current_start is None and start_detected:
            current_start = idx
        elif current_start is not None and (end_detected or idx == len(results) - 1):
            level_frame_ranges.append({"start": current_start, "end": idx})
            current_start = None

    return level_frame_ranges


def make_pacman_sprites(path, label_per_row, element_width, element_height, scale_width, scale_height):
    atlas = load_image(path, transparency = True)
    atlas_height, atlas_width, _ = atlas.shape
    n_element_rows = atlas_height // element_height
    n_element_cols = atlas_width  // element_width

    # Sanity check.
    if atlas_height % element_height:
        raise RuntimeError(f"loaded image with height not divisible by {element_height}: {atlas_height}")    
    if atlas_width % element_width:
        raise RuntimeError(f"loaded image with width not divisible by {element_width}: {atlas_width}")    
    if len(label_per_row) != n_element_rows:
        raise RuntimeError(f"expected one label per line in atlas. Instead got {len(label_per_row)} labels and {n_element_rows} rows of elements.")

    # Split atlas into sprites, removing fully-transparent sprites and duplicates per-row.
    sprites = []
    sprites_labels = []
    for idx_element_row in range(n_element_rows):
        top = idx_element_row * element_height
        label = label_per_row[idx_element_row]

        seen_in_element_row = set()
        for idx_element_col in range(n_element_cols):
            left = idx_element_col * element_width
            
            sprite = atlas[top:top + element_height, left:left + element_width]
            hashable = sprite.tobytes()

            if hashable in seen_in_element_row:
                continue
            if (sprite[:, :, -1] == 0).all(axis = None):
                continue
            
            seen_in_element_row.add(hashable)
            sprites.append(sprite)
            sprites_labels.append((label, idx_element_col))

    # Scale sprites.
    sprites = [resize_image(sprite, scale_width = scale_width, scale_height = scale_height) for sprite in sprites]

    return sprites, sprites_labels


def search_pacman(video_path, level_frame_ranges, maze_region, template_pacman_path, template_pacman_label_per_row, template_pacman_element_width, template_pacman_element_height, pacman_color_range_hsv, scale_width, scale_height):
    sprites, sprites_labels = make_pacman_sprites(template_pacman_path, template_pacman_label_per_row, template_pacman_element_width, template_pacman_element_height, scale_width, scale_height)

    callback = partial(search_pacman_callback_crop_frame, pacman_color_range_hsv = pacman_color_range_hsv, template_pacman_element_width = template_pacman_element_width, template_pacman_element_height = template_pacman_element_height)

    level_results = []
    for level in level_frame_ranges:
        res = match_template_whole_video(video_path, sprites, crop_frame_callback = callback, viewport = maze_region, frames_start = level["start"], frames_number = level["end"] - level["start"])
        level_results.append(res)

    return level_results, sprites_labels


def search_pacman_callback_crop_frame(frame, pacman_color_range_hsv, template_pacman_element_width, template_pacman_element_height):
    frame_height, frame_width, _ = frame.shape
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(converted, *pacman_color_range_hsv)
    rows, cols = mask.nonzero()
    if rows.size == 0:
        return None, None
    row_start = max(min(rows) - template_pacman_element_height    , 0)
    row_end   = min(max(rows) + template_pacman_element_height + 1, frame_height)
    col_start = max(min(cols) - template_pacman_element_width     , 0)
    col_end   = min(max(cols) + template_pacman_element_width  + 1, frame_width)
    return frame[row_start:row_end, col_start:col_end, :], Position(row = row_start, col = col_start)


def track_pacman_deaths(level_results, sprite_idx_of_label, detection_thr):
    def set_all_death_detections_to_invalid(level_results, sprite_idx_of_label, indices):
        if isinstance(indices, int):
            indices = [indices]
        
        for (label, _), sprite_idx in sprite_idx_of_label.items():
            if label == PacmanStates.DEATH:
                for idx in indices:
                    level_results[idx][sprite_idx] = MatchResults.NO_MATCH
        
        return level_results

    # Deaths are only valid if there the full sequence is present, with enough accuracy and remaining in the same place.
    death_current_label = None
    death_sequence_start_frame_idx = None
    death_sequences_detected = []
    for idx, frame_results in enumerate(level_results):
        death_next_label = (PacmanStates.DEATH, 0 if death_current_label is None else death_current_label[-1] + 1)

        if death_next_label not in sprite_idx_of_label:
            # We have detected a full sequence.
            death_sequences_detected.append((death_sequence_start_frame_idx, idx))
            death_current_label = None
            death_sequence_start_frame_idx = None
            continue
        
        detected_current_seq_step = (death_current_label is not None and
                                     frame_results[sprite_idx_of_label[death_current_label]].score <= detection_thr)
        detected_next_seq_step = frame_results[sprite_idx_of_label[death_next_label]].score <= detection_thr

        if detected_next_seq_step:
            # Move to search next step of sequence and, if we are on step 0, save where sequence started.
            death_current_label = death_next_label
            if death_sequence_start_frame_idx is None:
                death_sequence_start_frame_idx = idx

        else:
            if death_current_label is None:
                # Starting point of sequence not found. Then we can set all findings to invalid.
                level_results = set_all_death_detections_to_invalid(level_results, sprite_idx_of_label, idx)
            elif not detected_current_seq_step:
                # Retroactively invalidate death detections for all indices since we first suspected start of sequence.
                level_results = set_all_death_detections_to_invalid(level_results, sprite_idx_of_label, range(death_sequence_start_frame_idx, idx + 1))
            # If we are still at current step, don't do anything. Just keep searching.

    return level_results, death_sequences_detected




def track_pacman(pacman_search_results, sprites_labels, detection_thr):

    # Useful pre-processing: get labels-to-sprite index dictionary (reverse of sprites_labels).
    sprite_idx_of_label = {label: idx for idx, label in enumerate(sprites_labels)}

    for idx, level_results in enumerate(pacman_search_results):

        # Identifies frames between which a death occurred. Sets scores of death sprites to invalid if they are not part
        # of a detected sequence. This is done in-place.
        level_results, death_sequences_detected = track_pacman_deaths(level_results, sprite_idx_of_label, detection_thr)
        pacman_search_results[idx] = level_results
        if death_sequences_detected:
            raise NotImplementedError(f"Full death sequences have been detected between frames {death_sequences_detected}. This is not handled yet.")


        continue
    
    return level_results

    for _ in []:

        res_sorted = [
            MatchResults.NO_MATCH if frame_res == MatchResults.NO_MATCH else
            sorted(frame_res, key = lambda match: match.score)
            for frame_res in level_results
        ]

        print([np.nan if e == MatchResults.NO_MATCH else float(e[0].score) for e in res_sorted[:100]])
        print([np.nan if e == MatchResults.NO_MATCH else float(e[1].score) for e in res_sorted[:100]])


        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(4, 1)
        axes[0].plot([np.nan if e == MatchResults.NO_MATCH else e[0].score for e in res_sorted], label = "Score of 1st")
        axes[0].plot([np.nan if e == MatchResults.NO_MATCH else e[1].score for e in res_sorted], label = "Score of 2nd")
        axes[0].plot([np.nan if e == MatchResults.NO_MATCH else e[2].score for e in res_sorted], label = "Score of 3rd")
        axes[0].legend()

        axes[1].plot([np.nan if e == MatchResults.NO_MATCH else e[1].score / e[0].score for e in res_sorted], label = "Ratio Score 2nd / 1st")
        axes[1].legend()
        
        axes[2].plot([np.nan if e == MatchResults.NO_MATCH else e[1].score / e[0].score for e in res_sorted], label = "Ratio Score 3rd / 1st")
        axes[2].legend()
        
        axes[3].plot([np.nan if e == MatchResults.NO_MATCH else e[2].score / e[1].score for e in res_sorted], label = "Ratio Score 3rd / 2nd")
        axes[3].legend()
        plt.show()

        fig, axes = plt.subplots(4, 1)
        axes[0].hist([np.nan if e == MatchResults.NO_MATCH else e[0].score for e in res_sorted], bins = 30, alpha = 0.5, label = "Score of 1st")
        axes[0].hist([np.nan if e == MatchResults.NO_MATCH else e[1].score for e in res_sorted], bins = 30, alpha = 0.5, label = "Score of 2nd")
        axes[0].hist([np.nan if e == MatchResults.NO_MATCH else e[2].score for e in res_sorted], bins = 30, alpha = 0.5, label = "Score of 3rd")
        axes[0].legend()

        axes[1].hist([np.nan if e == MatchResults.NO_MATCH else e[1].score / e[0].score for e in res_sorted], bins = 30, label = "Ratio Score 2nd / 1st")
        axes[1].legend()
        
        axes[2].hist([np.nan if e == MatchResults.NO_MATCH else e[1].score / e[0].score for e in res_sorted], bins = 30, label = "Ratio Score 3rd / 1st")
        axes[2].legend()
        
        axes[3].hist([np.nan if e == MatchResults.NO_MATCH else e[2].score / e[1].score for e in res_sorted], bins = 30, label = "Ratio Score 3rd / 2nd")
        axes[3].legend()
        plt.show()





        analysed = []

        for res in [level_results]:
            
        # Handle: 
        # - Deaths are only valid if there is the full sequence afterwards with high enough accuracy. Otherwise put scores to infinity.
        # - Sometimes pacman disappears completely. In which case, assume position didn't change. 100 seems to be a good value for the thresholding of what is a reasonably accurate detection and what isn't. Additionally, some items are MatchResult.NO_MATCH.
        # - I see position jumping around sometimes.
            for sprite_idx, (label, _) in enumerate(sprites_labels):
                if label == "DEATH":
                    for idx, r in enumerate(res):
                        if r == MatchResults.NO_MATCH:
                            continue
                        res[idx][sprite_idx] = MatchResults(res[idx][sprite_idx], score = float("inf"))
            analysed.append(res)
    
    return analysed
    
        






if __name__ == "__main__":
    IDX = 2
    video_path = VIDEOS_PATHS[IDX]
    print(video_path)

    cache_path = f"cache_video_{IDX}.pkl"
    import os, pickle

    if os.path.isfile(cache_path):
        with open(cache_path, "rb") as file:
            viewport, scale_height, scale_width, maze_region, level_frame_ranges, pacman_search_results, pacman_search_labels = pickle.load(file)
    else:


        # ---------------------------------------------------------
        # ---------------------------------------------------------
        # ---------------------------------------------------------

        print("Finding viewport of video...")
        viewport = find_viewport(video_path)

        print("Finding scaling factors between video frames and templates...")
        scale_height, scale_width, maze_region = find_scale_and_maze_region(video_path,
                                                                            TEMPLATE_LEVEL_START_PATH,
                                                                            viewport)
        
        print("Detecting level start and end...")
        level_frame_ranges = find_start_end_levels(video_path,
                                                   TEMPLATE_LEVEL_START_PATH,
                                                   TEMPLATE_LEVEL_END_PATH,
                                                   maze_region,
                                                   scale_height,
                                                   scale_width,
                                                   LEVEL_START_END_DETECTION_THR)
        print(f"Found {len(level_frame_ranges)} levels.")

        print("Searching pacman in maze...")
        pacman_search_results, pacman_search_labels = search_pacman(video_path,
                                                                    level_frame_ranges[:1],
                                                                    maze_region,
                                                                    TEMPLATE_PACMAN_PATH,
                                                                    TEMPLATE_PACMAN_LABEL_PER_ROW,
                                                                    TEMPLATE_PACMAN_ELEMENT_WIDTH,
                                                                    TEMPLATE_PACMAN_ELEMENT_HEIGHT,
                                                                    PACMAN_COLOR_RANGE_HSV,
                                                                    scale_width,
                                                                    scale_height)
        

        # ---------------------------------------------------------
        # ---------------------------------------------------------
        # ---------------------------------------------------------

    # for frame in video_iterator(video_path, frames_start = level_frame_ranges[0]["start"], frames_number = level_frame_ranges[0]["end"] - level_frame_ranges[0]["start"]):
    #     converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #     mask = cv2.inRange(converted, *PACMAN_COLOR_RANGE_HSV)

    #     converted = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #     converted = np.hstack([converted, mask])

    #     cv2.imshow("", converted)
    #     if cv2.waitKey() == ord("q"):
    #         cv2.destroyAllWindows()
    #         break
    
    with open(cache_path, "wb") as file:
        pickle.dump((viewport, scale_height, scale_width, maze_region, level_frame_ranges, pacman_search_results, pacman_search_labels), file)


    print("Analysing search results to track pacman...")
    pacman_search_results = track_pacman(pacman_search_results,
                                         pacman_search_labels,
                                         PACMAN_DETECTION_THR)


    
    quit()

    print("Viewport:", viewport)
    print("Scale height:", scale_height)
    print("Scale width:", scale_width)
    print("Maze region:", maze_region)
    print("Number of levels:", len(level_frame_ranges))


    level = 0
    for result, frame in zip(pacman_search_results[level], 
                             video_iterator(video_path, frames_start = level_frame_ranges[level]["start"], frames_number = level_frame_ranges[level]["end"] - level_frame_ranges[level]["start"])):
        if result != MatchResults.NO_MATCH:
            sorted_idx = sorted(range(len(result)), key = lambda idx: result[idx].score)
            
            best_idx = sorted_idx[0]
            label = pacman_search_labels[best_idx]
            position = result[best_idx].pos + maze_region.start + Position(8, 8)        
            frame = cv2.circle(frame, center = (position.col, position.row), radius = 6, color = (0, 0, 255), thickness = -1)
            cv2.putText(frame, str(list(label) + [f"{result[best_idx].score:.2f}"]), (position.col + 5, position.row - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            best_idx = sorted_idx[1]
            label = pacman_search_labels[best_idx]
            position = result[best_idx].pos + maze_region.start + Position(8, 8)
            frame = cv2.circle(frame, center = (position.col, position.row), radius = 4, color = (0, 255, 0), thickness = -1)
            cv2.putText(frame, str(list(label) + [f"{result[best_idx].score:.2f}"]), (position.col + 5, position.row + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            best_idx = sorted_idx[2]
            label = pacman_search_labels[best_idx]
            position = result[best_idx].pos + maze_region.start + Position(8, 8)
            frame = cv2.circle(frame, center = (position.col, position.row), radius = 2, color = (255, 128, 0), thickness = -1)
            cv2.putText(frame, str(list(label) + [f"{result[best_idx].score:.2f}"]), (position.col + 5, position.row + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 128, 0), 1)


        cv2.imshow("", frame)
        if cv2.waitKey() == ord("q"):
            cv2.destroyAllWindows()
            break
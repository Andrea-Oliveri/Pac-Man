from functools import partial

import cv2
import numpy as np

from comparison_src.wrap_game_engine import GameFrames
from comparison_src.wrap_videos import Video
from comparison_src import analyse, utils


def _draw_frame(frame):
    frame = cv2.resize(
        frame,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_NEAREST
    )
    cv2.imshow("", frame)
    if cv2.waitKey(1) == ord("q"):
        quit()


def _find_viewport_and_scales(frame_generator_constructor, frames_to_search = 200, frames_step = 15):
    frame_generator_constructor = partial(
        frame_generator_constructor,
        frames_step = frames_step,
        frames_number = frames_to_search,
    )

    viewport = analyse.find_viewport(
        frame_generator_constructor()
    )

    scale_height, scale_width, maze_region = analyse.find_scale_and_maze_region(
        frame_generator_constructor(
            viewport = viewport
        )
    )

    print()
    print(viewport)
    print(f"{scale_height:.10f}, {scale_width:.10f}")
    print(maze_region)
    print(maze_region.height, maze_region.width)

    for frame in frame_generator_constructor():
        frame = cv2.rectangle(frame, (viewport.start.col, viewport.start.row), (viewport.stop.col, viewport.stop.row), (0,255,0), 2)
        frame = cv2.rectangle(frame, (maze_region.start.col, maze_region.start.row), (maze_region.stop.col, maze_region.stop.row), (0,0,255), 1)
        _draw_frame(frame)
    cv2.destroyAllWindows()

    return viewport, scale_height, scale_width, maze_region, frame



def _image_registration(img_src, rec_src, img_dst, rec_dst, pad_color):
    def _get_vertices(rec):
        return np.float32([
            (rec.start.row, rec.start.col),
            (rec.start.row, rec.stop.col),
            (rec.stop.row, rec.start.col),
        ])

    matrix = cv2.getAffineTransform(
        _get_vertices(rec_src),
        _get_vertices(rec_dst)
    )

    shrinking_width = matrix[0, 0] <= 1
    shrinking_height = matrix[1, 1] <= 1
    interpolation = utils.choose_best_interpolation(shrinking_width, shrinking_height)


    # TODO: debug how to make sure that the right portion of the post-transformation image is kept.


    dst_height, dst_width, _ = img_dst.shape
    img_src = cv2.warpAffine(
        img_src,
        matrix,
        dsize = (dst_width, dst_height),
        flags = interpolation,
        borderMode = cv2.BORDER_CONSTANT,
        borderValue = pad_color
    )


    mask_src = ~cv2.inRange(img_src, (0, 0, 0), (5, 5, 5))
    mask_dst = ~cv2.inRange(img_dst, (0, 0, 0), (5, 5, 5))

    overlapped = np.stack((mask_dst, mask_src, np.zeros_like(mask_src)), axis = -1)

    print(img_src.shape, img_src.dtype)
    print(img_dst.shape, img_dst.dtype)
    print(overlapped.shape, overlapped.dtype, overlapped.min(), overlapped.max())

    stacked = np.concatenate((img_src, img_dst, overlapped), axis = 1)
    cv2.imshow("", stacked)
    cv2.waitKey()
    cv2.destroyAllWindows()








if __name__ == "__main__":

    _find_viewport_and_scales = partial(_find_viewport_and_scales, frames_to_search = 15, frames_step = 60)


    video_path = R".\assets\videos\Pac-Man - Perfect Game 3333360.mp4"
    video_viewport, video_scale_height, video_scale_width, video_maze_region, video_frame = _find_viewport_and_scales(partial(Video, video_path = video_path))
    game_viewport, game_scale_height, game_scale_width, game_maze_region, game_frame = _find_viewport_and_scales(GameFrames)

    _image_registration(video_frame, video_maze_region, game_frame, game_maze_region, (0,0,0))

    quit()





    game = make_initial_game()

    for _ in range(400): # 400
        game = game.deepcopy()

        if game.event_update_state() is True:
            break
        frame = game.draw()

        _draw_frame(frame)

    cv2.destroyAllWindows()

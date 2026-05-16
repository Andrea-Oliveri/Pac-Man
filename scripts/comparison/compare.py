from functools import partial

import cv2

from comparison_src.wrap_game_engine import GameFrames, Game
from comparison_src.wrap_videos import Video
from comparison_src import analyse



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
    frames_generator = frame_generator_constructor(frames_step = frames_step, frames_number = frames_to_search, progress_bar = True)
    viewport = analyse.find_viewport(frames_generator)

    frames_generator.viewport = viewport
    scale_height, scale_width, _ = analyse.find_scale_and_maze_region(frames_generator)

#    return viewport, scale_height, scale_width

    for frame in frames_generator:
        frame = cv2.rectangle(frame, (viewport.start.col, viewport.start.row), (viewport.stop.col, viewport.stop.row), (0,255,0), 2)
        frame = cv2.rectangle(frame, (_.start.col, _.start.row), (_.stop.col, _.stop.row), (0,0,255), 1)
        _draw_frame(frame)

    print(viewport)
    print(scale_height, scale_width)

    return viewport, scale_height, scale_width



if __name__ == "__main__":
    video_path = R".\assets\videos\recording2.avi"
    #video_viewport, video_scale_height, video_scale_width = _find_viewport_and_scales(partial(Video, video_path = video_path))
    game_viewport, game_scale_height, game_scale_width = _find_viewport_and_scales(GameFrames)

    quit()





    game = make_initial_game()

    for _ in range(400): # 400
        game = game.deepcopy()

        if game.event_update_state() is True:
            break
        frame = game.draw()

        _draw_frame(frame)

    cv2.destroyAllWindows()

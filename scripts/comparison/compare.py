import cv2

from comparison_src.wrap_game_engine import make_initial_game
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


def _find_video_viewport_and_scales(video_path, frames_to_search = 200, frames_step = 15):
    video = Video(video_path, frames_step = frames_step, frames_number = frames_to_search)
    viewport = analyse.find_viewport(video)

    video.viewport = viewport
    scale_height, scale_width, _ = analyse.find_scale_and_maze_region(video)

    return viewport, scale_height, scale_width

    for frame in video:
        frame = cv2.rectangle(frame, (viewport.start.col, viewport.start.row), (viewport.stop.col, viewport.stop.row), (0,255,0), 2)
        frame = cv2.rectangle(frame, (mz.start.col, mz.start.row), (mz.stop.col, mz.stop.row), (0,0,255), 1)
        _draw_frame(frame)

    print(viewport)
    print(scale_height, scale_width)


def _find_game_viewport_and_scales(frames_to_search = 200, frames_step = 15):
    viewport = analyse.find_viewport(_yield_game_frames(frames_to_search, frames_step))

    scale_height, scale_width, mz = analyse.find_scale_and_maze_region(_yield_game_frames(frames_to_search, frames_step, viewport))

    #return viewport, scale_height, scale_width

    for frame in _yield_game_frames(frames_to_search, frames_step):
        frame = cv2.rectangle(frame, (viewport.start.col, viewport.start.row), (viewport.stop.col, viewport.stop.row), (0,255,0), 2)
        frame = cv2.rectangle(frame, (mz.start.col, mz.start.row), (mz.stop.col, mz.stop.row), (0,0,255), 1)
        _draw_frame(frame)

    print(viewport)
    print(scale_height, scale_width)




def _yield_game_frames(frames_to_search, frames_step, viewport = None):
    if not isinstance(frames_to_search, int) or frames_to_search < 0:
        raise RuntimeError(f"Parameter frames_to_search must be a positive integer. Got {frames_to_search}")
    if not isinstance(frames_step, int) or frames_step < 0:
        raise RuntimeError(f"Parameter frames_step must be a positive integer. Got {frames_step}")

    game = make_initial_game()

    last_frame = (frames_to_search - 1) * frames_step
    frame_number = -1

    while game.event_update_state() is not True:
        frame_number += 1
        if frame_number % frames_step == 0:
            frame = game.draw()
            if viewport is not None:
                frame = frame[viewport.start.row:viewport.stop.row, viewport.start.col:viewport.stop.col]
            yield frame
        if frame_number >= last_frame:
            break







if __name__ == "__main__":
    video_path = R".\assets\videos\recording2.avi"
    video_viewport, video_scale_height, video_scale_width = _find_video_viewport_and_scales(video_path)

    _find_game_viewport_and_scales()

    quit()





    game = make_initial_game()

    for _ in range(400): # 400
        game = game.deepcopy()

        if game.event_update_state() is True:
            break
        frame = game.draw()

        _draw_frame(frame)

    cv2.destroyAllWindows()

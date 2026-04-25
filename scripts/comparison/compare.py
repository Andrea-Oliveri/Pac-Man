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
    video = Video(video_path, frames_step = frames_step, frames_number = frames_to_search, progress_bar=True)
    viewport = analyse.find_viewport(video)

    video.viewport = viewport
    scale_height, scale_width, mz = analyse.find_scale_and_maze_region(video)

    for frame in video:
        frame = cv2.rectangle(frame, (viewport.start.col, viewport.start.row), (viewport.stop.col, viewport.stop.row), (0,255,0), 2)
        frame = cv2.rectangle(frame, (mz.start.col, mz.start.row), (mz.stop.col, mz.stop.row), (0,0,255), 1)
        _draw_frame(frame)

    print(viewport)
    print(scale_height, scale_width)


if __name__ == "__main__":
    video_path = R".\assets\videos\recording2.avi"
    _find_video_viewport_and_scales(video_path)
    quit()



    for frame in video:
        _draw_frame(frame)

    cv2.destroyAllWindows()



    game = make_initial_game()

    for _ in range(400): # 400
        game = game.deepcopy()

        if game.event_update_state() is True:
            break
        frame = game.draw()

        _draw_frame(frame)

    cv2.destroyAllWindows()

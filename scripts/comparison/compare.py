import cv2

from src.wrap_game_engine import make_initial_game
from src.wrap_videos import Video



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




game = make_initial_game()

for _ in range(400): # 400
    game = game.deepcopy()

    if game.event_update_state() is True:
        break
    frame = game.draw()

    _draw_frame(frame)

cv2.destroyAllWindows()




video = Video(R".\assets\videos\recording2.avi")

for frame in video:
    _draw_frame(frame)

cv2.destroyAllWindows()


import cv2


def choose_best_interpolation(shrinking_width, shrinking_height):
    return (
        cv2.INTER_AREA if shrinking_width and shrinking_height
        else cv2.INTER_LANCZOS4
    )
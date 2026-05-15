import cv2
import numpy as np


TEMPLATE_LEVEL_END_PATH = "../assets/images/level_end.png"
MAZE_TILE_SIZE_PX = 8
BLACK_VALUE_THR = 5
TOLERANCE_PX = 2
OUTPUT_PATH = "../assets/images/valid_pacman_positions.png"


def _check_if_out_of_bounds(image, row, col):
    return row < 0 or row >= image.shape[0] or col < 0 or col >= image.shape[1]


def _get_tile(image, row, col, raise_if_out_of_bounds = True, tile_rows = MAZE_TILE_SIZE_PX, tile_cols = MAZE_TILE_SIZE_PX):
    if _check_if_out_of_bounds(image, row, col):
        if raise_if_out_of_bounds:
            raise ValueError(f"Can't get out-of-bounds tile: image has shape {image.shape} but requested row {row} and column {col}")
        else:
            return None
    return image[row:row+tile_rows, col:col+tile_cols]


def _set_tile(image, row, col, value, tile_rows = MAZE_TILE_SIZE_PX, tile_cols = MAZE_TILE_SIZE_PX):
    if _check_if_out_of_bounds(image, row, col):
        raise ValueError(f"Can't set out-of-bounds tile: image has shape {image.shape} but requested row {row} and column {col}")
    image[row:row+tile_rows, col:col+tile_cols] = value
    return image


def _tile_contains_wall(mask_invalid, row, col, **kwargs):
    tile = _get_tile(mask_invalid, row, col, **kwargs)
    return tile is None or np.any(tile)



mask_invalid = cv2.imread(TEMPLATE_LEVEL_END_PATH, cv2.IMREAD_COLOR)
mask_nrows, mask_ncols, _ = mask_invalid.shape

# Flatten color channels to a single one.
mask_invalid = cv2.inRange(mask_invalid, (0, 0, 0), (BLACK_VALUE_THR, BLACK_VALUE_THR, BLACK_VALUE_THR)) == 0

for tile_row in range(0, mask_nrows, MAZE_TILE_SIZE_PX):
    for tile_col in range(0, mask_ncols, MAZE_TILE_SIZE_PX):

        # If tile contains a maze wall, mark the whole tile as an invalid position for Pacman.        
        if _tile_contains_wall(mask_invalid, tile_row, tile_col):
            mask_invalid = _set_tile(mask_invalid, tile_row, tile_col, True)
        
        # Otherwise we mark all invalid except the pixels where the upper-left of the Pacman sprite can go.
        else:
            top_valid = False
            left_valid = False

            left_tile_origin = (tile_row, tile_col - MAZE_TILE_SIZE_PX)
            right_tile_origin = (tile_row, tile_col + MAZE_TILE_SIZE_PX)
            above_tile_origin = (tile_row - MAZE_TILE_SIZE_PX, tile_col)
            below_tile_origin = (tile_row + MAZE_TILE_SIZE_PX, tile_col)

            for tile in left_tile_origin, right_tile_origin:
                if not _tile_contains_wall(mask_invalid, *tile, raise_if_out_of_bounds = False):
                    top_valid = True
                    break
            for tile in above_tile_origin, below_tile_origin:
                if not _tile_contains_wall(mask_invalid, *tile, raise_if_out_of_bounds = False):
                    left_valid = True
                    break
            
            mask_invalid = _set_tile(mask_invalid, tile_row, tile_col, True)
            if top_valid:
                mask_invalid = _set_tile(mask_invalid, tile_row, tile_col, False, tile_rows = TOLERANCE_PX)
            if left_valid:
                mask_invalid = _set_tile(mask_invalid, tile_row, tile_col, False, tile_cols = TOLERANCE_PX)

print("WARNING: manual adjustments are still required")
cv2.imwrite(OUTPUT_PATH, (~mask_invalid).astype("uint8") * 255)
del mask_invalid

mask_valid = cv2.imread(OUTPUT_PATH, cv2.IMREAD_GRAYSCALE) > 0
template = cv2.imread(TEMPLATE_LEVEL_END_PATH, cv2.IMREAD_COLOR)
template[mask_valid] = [0, 0, 255]
cv2.imshow("Mask Valid (red) on Reference Image", template)
cv2.waitKey()
cv2.destroyAllWindows()
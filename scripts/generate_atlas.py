"""
This script converts a series of images into a single image atlas.
Additionally, a text file is stored describing the coordinates and size of the images stored in the atlas.

This script was used to generate a unified atlas from separate image files stored in assets.

Usage:
1)   Since this script uses packages not used in the main project, these may need to be installed before running. To do so, run:
          pip install opencv-python

2)   Edit the IMAGE_PATHS, ATLAS_IMG_FILENAME, REGIONS_TXT_FILENAME, BORDER_SIZE_PX and ATLAS_DIMS_PX variables in this script.

3)   Run the script:
          python ./generate_atlas.py
"""





import pyglet
import cv2
import os


# List of images to group together in atlas.
IMAGE_PATHS = ['../assets/images/Font.png',
               '../assets/images/Ghosts.png',
               '../assets/images/Maze Initial.png',
               '../assets/images/Maze Flash Blue.png',
               '../assets/images/Maze Flash White.png',
               '../assets/images/Pac-Man.png',
               '../assets/images/Scores.png',
               '../assets/images/UI.png']

# Output filename of generated atlas.
ATLAS_IMG_FILENAME = './atlas.png'

# Output filename where to store the coordinates of the top-left vertex of each image in atlas, as well as its width and height.
REGIONS_TXT_FILENAME = './regions.txt'

# Number of pixels to add to the border of each image in atlas using and replicating the external pixels to fill the border.
BORDER_SIZE_PX = 0

# Dimention of the texture atlas as (width, height).
ATLAS_DIMS_PX = (1024, 512)









# Add border to each image and load them into list.
tempfile = './temp.png'
images = {}
for im_p in IMAGE_PATHS:
    im = cv2.imread(im_p, cv2.IMREAD_UNCHANGED)
    im = cv2.copyMakeBorder(im, top=BORDER_SIZE_PX, bottom=BORDER_SIZE_PX, left=BORDER_SIZE_PX, right=BORDER_SIZE_PX, borderType=cv2.BORDER_REPLICATE)

    cv2.imwrite(tempfile, im)
    im = pyglet.image.load(tempfile)

    images[im_p] = im
os.remove(tempfile)

# Create atlas and add images.
atlas = pyglet.image.atlas.TextureAtlas(*ATLAS_DIMS_PX)
images = dict(sorted(images.items(), key = lambda e: e[1].height, reverse = True)) # Sort in decreasing height order for best performance of atlas allocation.
images = {im_p: atlas.add(im) for im_p, im in images.items()}


# Calculate coords and sizes of each element in atlas.
coords_and_sizes = ['Path: (X_left, Y_bottom, Width, Height)']
max_path_len = max(len(p) for p in images.keys())
for im_p, im in images.items():
    coords_and_sizes.append(f"{im_p:<{max_path_len}}:   ({im.x + BORDER_SIZE_PX}, {im.y + BORDER_SIZE_PX}, {im.width - 2*BORDER_SIZE_PX}, {im.height - 2*BORDER_SIZE_PX})")
coords_and_sizes = '\n'.join(coords_and_sizes)


# Save image and file.
atlas.texture.save(ATLAS_IMG_FILENAME)
with open(REGIONS_TXT_FILENAME, 'w') as file:
    file.write(coords_and_sizes)
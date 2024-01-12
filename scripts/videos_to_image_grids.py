"""
This script converts a video into a series of images. 
Each image is a collage of video frames stacked vertically.

The output images is stored both as raw image and as lzma-compressed image data.
Additionally, a text file is stored describing the number of frames and frame shape for each output image.

This script was used to convert recordings into series of images now present inside of assets folder (used for intermissions and intro).

Usage:
1)   Since this script uses packages not used in the main project, these may need to be installed before running. To do so, run:
          pip install opencv-python

2)   Edit the FRAMES_RANGES and (optionally) SHAPES_TXT_FILENAME variables in this script.

3)   Run the script:
          python ./videos_to_image_grids.py
"""





import cv2
import numpy as np
import os
import lzma


# Dictionary with, as keys, the video file to convert.
# As values, the different image grids to generate for each video.
# Each tuple consists of: (filename of output image, start frame to include in output, end frame to include in output, number of pixels to crop from top and bottom)
FRAMES_RANGES = {
                     './recording.avi': 
                         [
                             ('intermission1.png', 1018, 1671, 100),
                             ('intermission2.png', 2356, 2884, 100),
                             ('intermission3.png', 3802, 4341, 100)
                         ],

                     './recording_attract.avi': 
                         [
                             ('intro.png'  , 295 , 1510, 40),
                             ('attract.png', 1515, 4706, 16),
                         ]
                 }

# Output filename where to store, for each output image the following:
# (number of frames, number of rows of each frame, width of each frame)
SHAPES_TXT_FILENAME = './shapes.txt'





if os.path.isfile(SHAPES_TXT_FILENAME):
    os.remove(SHAPES_TXT_FILENAME)


for video_path, names_and_ranges in FRAMES_RANGES.items():

    cap = cv2.VideoCapture(video_path)

    for filename, start, end, crop_top_and_bottom in names_and_ranges:

        start    = int(start)
        n_frames = int(end) - start 

        cap.set(cv2.CAP_PROP_POS_FRAMES, start)
    
        frames = []
        for i in range(n_frames):
            _, frame = cap.read()

            if crop_top_and_bottom > 0:
                frame = frame[crop_top_and_bottom:-crop_top_and_bottom, :]
            frames.append(frame)


        with open(SHAPES_TXT_FILENAME, 'a') as file:
            file.write(f'{filename} frame shape: {[len(frames), *frames[0].shape]}\n')
            

        frames = np.concatenate(frames, axis=0)

        cv2.imwrite(filename, frames, [cv2.IMWRITE_PNG_COMPRESSION, 9])
        



filenames = [e[0] for l in FRAMES_RANGES.values() for e in l]

for name in filenames:
    with open(name, "rb") as f:
        data = f.read()
    with lzma.open(name + ".xz", "wb") as f:
        f.write(data)


    import time
    print(name)
    s = time.time()
    with lzma.open(name + ".xz", "rb") as f:
        data = f.read()
    print(time.time() - s, 'seconds to decompress')
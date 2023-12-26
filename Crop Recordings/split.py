import cv2
import numpy as np
import os
import lzma


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

SHAPES_TXT_FILENAME = 'shapes.txt'


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
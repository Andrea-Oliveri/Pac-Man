"""
This script generate a sound file repeating multiple times the input sound file.

The output is stored both raw and lzma-compressed.

This script was used to loop siren sounds many times over to reduce artefacts due to not gapless looping implemented by Pyglet.

Usage:
1)   Since this script uses packages not used in the main project, these may need to be installed before running. To do so, run:
          pip install scipy

2)   Edit the SOUND_WAV_FIELS, OUT_FOLDER and NUM_REPEATS variables in this script.

3)   Run the script:
          python ./loop_sounds.py
"""





import scipy
import numpy as np
import lzma
import os


# List of sound effects to loop.
SOUND_WAV_FIELS = ['./power_pellet.wav',
                   './retreating.wav',
                   './siren_1.wav',
                   './siren_2.wav',
                   './siren_3.wav',
                   './siren_4.wav',
                   './siren_5.wav']

# Folder in which to store the output files.
OUT_FOLDER = './Out'

# Integer stating the number of times each sound must be repeated in output.
NUM_REPEATS = 10





os.makedirs(OUT_FOLDER, exist_ok = True)
out_paths = []

for p in SOUND_WAV_FIELS:
    rate, sound = scipy.io.wavfile.read(p)

    sound = np.tile(sound, NUM_REPEATS)

    out_path = os.path.join(OUT_FOLDER, os.path.basename(p))
    out_paths.append(out_path)

    scipy.io.wavfile.write(out_path, rate, sound)



for p in out_paths:
    with open(p, "rb") as f:
        data = f.read()
    with lzma.open(p + ".xz", "wb") as f:
        f.write(data)

    
    import time
    print(p)
    s = time.time()
    with lzma.open(p + ".xz", "rb") as f:
        data = f.read()
    print(time.time() - s, 'seconds to decompress')



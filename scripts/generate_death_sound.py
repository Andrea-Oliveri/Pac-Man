"""
This script converts a series of images into a single image atlas.
Additionally, a text file is stored describing the coordinates and size of the images stored in the atlas.

This script was used to generate a unified atlas from separate image files stored in assets.

Usage:
1)   Since this script uses packages not used in the main project, these may need to be installed before running. To do so, run:
          pip install scipy tqdm

2)   Edit the DEATH_1_WAV_PATH, DEATH_2_WAV_PATH, REFERENCE_WAV_PATH and OUTPUT_WAV_PATH variables in this script.

3)   Run the script:
          python ./generate_death_sound.py
"""




import scipy
import numpy as np
from tqdm import tqdm


# WAV file containing the first part of death sound effect.
DEATH_1_WAV_PATH   = '../references/original assets/sounds/death_1.wav'

# WAV file containing the second part of death sound effect.
DEATH_2_WAV_PATH   = '../references/original assets/sounds/death_2.wav'

# WAV file containing the reference recording of the death sound effect.
REFERENCE_WAV_PATH = './death.wav'

# Desired path of output WAV file.
OUTPUT_WAV_PATH    = './out.wav'




# Load wav files.
rate_1  , death_1   = scipy.io.wavfile.read(DEATH_1_WAV_PATH)
rate_2  , death_2   = scipy.io.wavfile.read(DEATH_2_WAV_PATH)
rate_ref, reference = scipy.io.wavfile.read(REFERENCE_WAV_PATH)



# Sanity checks.
assert rate_2 == rate_1
rate_out = rate_1
del rate_1, rate_2

assert death_1.ndim == death_2.ndim == reference.ndim == 1


# Creation of variables for optimization ranges.
len_output_signal = int((reference.size / rate_ref) * rate_out)
ref_timepoints    = np.arange(reference.size)
out_timepoints    = np.arange(len_output_signal)


# Optimize to find best fit.
def paste_slice(destination, start, end, source):
    end = min(end, destination.size)
    l   = end - start
    destination[start:end] = source[:l]
    destination[end:] = 0
    return destination


def build_from_params(start_idx_death_1, start_idx_death_2_first, start_idx_death_2_second):
    start_idx_death_1        = int(start_idx_death_1)
    start_idx_death_2_first  = int(start_idx_death_2_first)
    start_idx_death_2_second = int(start_idx_death_2_second)

    end_idx_death_1          = start_idx_death_1        + death_1.size
    end_idx_death_2_first    = start_idx_death_2_first  + death_2.size
    end_idx_death_2_second   = start_idx_death_2_second + death_2.size

    s = np.zeros(len_output_signal, dtype = death_1.dtype)
    s = paste_slice(s, start_idx_death_1       , end_idx_death_1       , death_1)
    s = paste_slice(s, start_idx_death_2_first , end_idx_death_2_first , death_2)
    s = paste_slice(s, start_idx_death_2_second, end_idx_death_2_second, death_2)

    return s


def calculate_corr(params):
    s = build_from_params(*params)

    s_resampled = np.interp(ref_timepoints, out_timepoints, s, left = 0, right = 0)
    corr, = scipy.signal.correlate(reference, s_resampled, mode = 'valid')
    
    return corr


def brute_force(range_start_idx_death_1, range_start_idx_death_2_first, range_start_idx_death_2_second):
    best = (-float('inf'), None)

    for start_idx_death_1 in tqdm(range_start_idx_death_1, leave = False):
        for start_idx_death_2_first in tqdm(range_start_idx_death_2_first, leave = False):
            for start_idx_death_2_second in tqdm(range_start_idx_death_2_second, leave = False):
                params = (start_idx_death_1, start_idx_death_2_first, start_idx_death_2_second)

                res = calculate_corr(params)
                
                if res > best[0]:
                    best = (res, params)
    
    return best


def generate_ranges(step_now, x0 = None, step_before = None):
    if x0 is None:
        return [range(0, len_output_signal // 2, step_now),
                range(len_output_signal // 2, len_output_signal - 2 * death_2.size, step_now),
                range(len_output_signal // 2, len_output_signal - 1 * death_2.size, step_now)]

    return [range(x0_i - step_before, x0_i + step_before, step_now) for x0_i in x0]




step = 1000
x = None
step_before = None

while step >= 1:
    ranges = generate_ranges(step, x, step_before)
    _, x = brute_force(*ranges)
    
    step_before = step
    step //= 10
    

out = build_from_params(*x)
scipy.io.wavfile.write(OUTPUT_WAV_PATH, rate_out, out)

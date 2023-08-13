from src.constants import (PRNG_ROM_MEM,
                           PRNG_BITS_TO_DIRECTION)


class PRNG:

    def __init__(self):
        self.rng_index = 0


    def reset(self):
        self.rng_index = 0


    def get_random_direction(self):
        # Implemented as described in https://www.youtube.com/watch?v=eFP0_rkjwlY and https://www.reddit.com/r/Pacman/comments/14qu2vy/how_do_i_copy_this_thing_used_in_the_rng/

        self.rng_index = ((self.rng_index * 5) + 1) % 8192

        mem_byte = PRNG_ROM_MEM[self.rng_index]
        lsb = int(mem_byte, base = 16) & 0b00000011

        return PRNG_BITS_TO_DIRECTION[lsb]
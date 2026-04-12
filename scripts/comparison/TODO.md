Decide approach:
1) Continue analyse original to track pacman and make a list of moves
--- Probably harder
--- Approaches to continue work described in .py
2) Work on compare.py
--- Use techniques developed in analyse_original.py to, for each frame, align them and find how well they correspond
--- Need to explore all options: move in each (valid direction) or no move, for each frame
--- Need to keep tree of 10-20-30 frames dynamically and explore all options to know which one matches best
--- Need to highlight differences between two video streams
--- Problem: how to parallelize (OpenGL wants rendering always in main thread. Perhaps ProcessPoolExecutors since they will have a main thread of their own)
# -*- coding: utf-8 -*-

import os
import sys

# Needed for compatibility with pyinstaller.
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)


import pyglet

# This improves stability by preventing strange occasional crashes when creating main window.
# It also appears to avoid other occasional issue where process takes long time to end after window closed.
# See GitHub issue pyglet/pyglet#1019
pyglet.options['shadow_window'] = False



from src.window import Window

window = Window()

pyglet.app.run()

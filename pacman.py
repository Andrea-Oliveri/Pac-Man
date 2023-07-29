# -*- coding: utf-8 -*-

import os
import sys

# Needed for compatibility with pyinstaller.
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)



import pyglet.app
from src.window import Window

window = Window()

pyglet.app.run()

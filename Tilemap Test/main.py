import pyglet
pyglet.options['shadow_window'] = False

from window import Window
w = Window()
pyglet.app.run()
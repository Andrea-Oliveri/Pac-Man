
import pyglet


N_ROWS = 36
N_COLS = 28
TILE_PX_SIZE = 8


class TileMap:

    def __init__(self):
        self._texture   = pyglet.image.load('Font.png').get_texture()
        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, self._texture.id)
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
        
        self._max_value = (self._texture.width // TILE_PX_SIZE) * (self._texture.height // TILE_PX_SIZE) - 1

        self._map = [0] * N_ROWS * N_COLS

    def _cvt_idx(self, idx):
        row, col = idx

        if row > N_ROWS or row < 0:
            raise IndexError
        if col > N_COLS or col < 0:
            raise IndexError
        return row * N_COLS + col

    def __getitem__(self, idx):
        idx = self._cvt_idx(idx)
        return self._map[idx]

    def __setitem__(self, idx, value):
        idx = self._cvt_idx(idx)

        if value > self._max_value or value < 0:
            raise IndexError

        self._map[idx] = value

    def __len__(self):
        return len(self._map)
    


    def random_fill(self):
        from random import randint

        for row in range(N_ROWS):
            for col in range(N_COLS):
                self[row, col] = randint(0, self._max_value)
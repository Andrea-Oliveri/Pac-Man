# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod



class AbstractSprite(ABC):

    def __init__(self, painter):

        # Store painter to add vertex data when drawing.
        self._painter = painter

        self.reset()

    @abstractmethod
    def reset(self):
        return

    @abstractmethod
    def update(self):
        return

    @abstractmethod
    def send_vertex_data(self):
        return
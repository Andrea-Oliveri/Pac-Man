# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import ClassVar


# --------------------------------------------------------------------
# Vector2 dataclass.
# --------------------------------------------------------------------

@dataclass(slots = True, eq = True)
class Vector2:
    # x coordinate represent right-left direction, with positive values being towards the right.
    x: float

    # y coordinate represent right-left direction, with positive values being towards the top.
    y: float

    # Function returning a new Vector2 instance which has the x and y coordinates swapped.
    def swap(self):
        return Vector2(self.y, self.x)

    # Operator overloadings.
    def __add__(self, other):
        if not isinstance(other, Vector2):
            self.raise_typerror('+', self, other)

        return Vector2(x = self.x + other.x,
                       y = self.y + other.y)

    def __iadd__(self, other):
        if not isinstance(other, Vector2):
            self.raise_typerror('+=', self, other)

        self.x += other.x
        self.y += other.y
        return self

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            self.raise_typerror('*', self, other)

        return Vector2(x = self.x * other,
                       y = self.y * other)

    def __imul__(self, other):
        if not isinstance(other, (int, float)):
            self.raise_typerror('*=', self, other)

        self.x *= other
        self.y *= other
        return self

    @staticmethod
    def raise_typerror(operator, left_obj, right_obj):
        left_type_name  = left_obj .__class__.__name__
        right_type_name = right_obj.__class__.__name__

        raise TypeError(f"unsupported operand type(s) for {operator}: '{left_type_name}' and '{right_type_name}'")


# Static variables for ease of use.
Vector2.LEFT  = Vector2(-1, 0)
Vector2.RIGHT = Vector2(+1, 0)
Vector2.UP    = Vector2(0, +1)
Vector2.DOWN  = Vector2(0, -1)

# --------------------------------------------------------------------

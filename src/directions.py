# -*- coding: utf-8 -*-

from dataclasses import dataclass

# --------------------------------------------------------------------
# Vector2 dataclass.
# --------------------------------------------------------------------

@dataclass(slots = True, eq = True)
class Vector2:
    # x coordinate represent right-left direction, with positive values being towards the right.
    x: float

    # y coordinate represent right-left direction, with positive values being towards the top.
    y: float

    # Operator overloadings. Inplace operations should not modify the instance herself to
    # avoid accidentally changing the LEFT, RIGHT, UP, DOWN contants. 
    def __add__(self, other):
        if not isinstance(other, Vector2):
            self.raise_typerror('+', self, other)

        return Vector2(x = self.x + other.x,
                       y = self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector2):
            self.raise_typerror('-', self, other)

        return Vector2(x = self.x - other.x,
                       y = self.y - other.y)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            self.raise_typerror('*', self, other)

        return Vector2(x = self.x * other,
                       y = self.y * other)

    def __neg__(self):
        return Vector2(x = -self.x,
                       y = -self.y)

    def __rmul__(self, other):
        return self * other


    def __hash__(self):
        return hash((self.x, self.y))


    def round_to_nearest_half(self):
        return Vector2(x = round(self.x * 2) / 2,
                       y = round(self.y * 2) / 2)


    @staticmethod
    def distance_squared(left_obj, right_obj):
        if not isinstance(left_obj, Vector2) or not isinstance(right_obj, Vector2):
            Vector2.raise_typerror('distance_squared', left_obj, right_obj)

        return (left_obj.x - right_obj.x) ** 2 + (left_obj.y - right_obj.y) ** 2


    @staticmethod
    def raise_typerror(operator, left_obj, right_obj):
        left_type_name  = left_obj .__class__.__name__
        right_type_name = right_obj.__class__.__name__

        raise TypeError(f"unsupported operand type(s) for {operator}: '{left_type_name}' and '{right_type_name}'")


# Static variables for ease of use.
Vector2.LEFT  = Vector2(-1, 0)
Vector2.RIGHT = Vector2(+1, 0)
Vector2.UP    = Vector2(0, -1)
Vector2.DOWN  = Vector2(0, +1)
Vector2.ZERO  = Vector2(0, 0)

# --------------------------------------------------------------------
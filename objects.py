from ursina import *
from random import randrange

class Bricks(Entity):
    def __init__(self, MAP_SIZE, i, j, **kwargs):
        super().__init__(**kwargs)
        self.i = i
        self.j = j
        self.MAP_SIZE = MAP_SIZE
        self.new_position()

    def new_position(self):
        self.position = (self.MAP_SIZE - (self.i * 2) - 1, self.MAP_SIZE - (self.j * 1.2) - 1, -0.5)


class Paddle(Entity):
    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.new_position()

    def new_position(self):
        self.position = (self.MAP_SIZE // 2, 1, -0.5)

class Ball(Entity):
    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.new_position()

    def new_position(self):
        self.position = (self.MAP_SIZE // 2, 4, -0.5)
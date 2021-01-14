import numpy as np
from pygame import draw


class Particle:
    def __init__(self, position, radius):
        self.x = position[0]
        self.y = position[1]
        self.highlight = False
        self.r = radius

    def move(self, max_x, max_y):
        self.x += 2*np.random.rand()-1
        self.y += 2*np.random.rand()-1
        if self.x <= 0:
            self.x = 0
        if self.x >= max_x:
            self.x = max_x
        if self.y <= 0:
            self.y = 0
        if self.y >= max_y:
            self.y = max_y
        self.highlight = False

    def render(self, window):
        if self.highlight:
            draw.circle(window, (0, 255, 0), (self.x, self.y), self.r)
        else:
            draw.circle(window, (255, 255, 255), (self.x, self.y), self.r)

    def check_collision(self, others):
        for other in others:
            if self != other:
                distance_squared = (self.x - other.x)**2 + (self.y - other.y)**2
                if distance_squared < (other.r + self.r)**2:
                    self.highlight = True
                    other.highlight = True

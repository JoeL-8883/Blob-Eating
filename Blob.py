import math
import pygame
import threading
import random
import time

class Blob:
    def __init__(self, x, y, radius, colour, lifetime):
        self.x = x
        self.y = y
        self.radius = radius
        self.size = math.pi * self.radius ** 2
        self.colour = colour
        self.birth = time.time()
        self.lifetime = lifetime

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), int(self.radius))

    def die(self):
        if time.time() - self.birth > self.lifetime:
            return True
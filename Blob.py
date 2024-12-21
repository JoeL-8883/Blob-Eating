import math
import pygame

class Blob:
    def __init__(self, x, y, radius, colour):
        self.x = x + 5
        self.y = y + 5
        self.radius = radius
        self.size = math.pi * self.radius ** 2
        self.colour = colour

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), int(self.radius))

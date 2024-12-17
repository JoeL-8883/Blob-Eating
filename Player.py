import pygame
import math

class Player:
    def __init__(self, x, y, radius, colour, speed, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.size = math.pi * self.radius ** 2
        self.colour = colour
        self.speed = speed
        self.name = name
    
    def move(self, dx, dy, map_size):
        self.x += dx
        self.y += dy

        if self.x < self.radius:
            self.x = self.radius
        if self.y < self.radius:
            self.y = self.radius
        if self.x > map_size - self.radius:
            self.x = map_size - self.radius
        if self.y > map_size - self.radius:
            self.y = map_size - self.radius

    def draw(self, screen, font, x, y):
        pygame.draw.circle(screen, self.colour, (x, y), self.radius-1)
        outer_c = (self.colour[0] - 10, self.colour[1] - 10, self.colour[2] - 10)
        pygame.draw.circle(screen, outer_c, (x, y), self.radius, 4) # Outer circle
        label_surface = font.render(self.name, True, (0, 0, 0))
        screen.blit(label_surface, (x, y))
    
    def distance(self, x, y):
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def can_eat_blob(self, blob):
        if self.distance(blob.x, blob.y) < self.radius + blob.radius:
            return True
    
    def eat_blob(self, blob):
        self.size += blob.size
        self.radius = math.sqrt(self.size / math.pi)
        
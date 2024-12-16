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
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def draw(self, screen, font):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)
        label_surface = font.render(self.name, True, (255, 255, 255))
        screen.blit(label_surface, (self.x - self.radius, self.y - self.radius - 20))

    def can_eat_blob(self, blob):
        distance = math.sqrt((self.x - blob.x) ** 2 + (self.y - blob.y) ** 2)
        if distance < self.radius + blob.radius:
            return True
    
    def eat_blob(self, blob):
        self.size += blob.size
        self.radius = math.sqrt(self.size / math.pi)
        
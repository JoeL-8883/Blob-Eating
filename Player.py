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
        self.font = pygame.font.SysFont("arial", self.font_size())

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

    def font_size(self):
        return int(self.size/(self.radius*5))

    def draw(self, screen, x, y):
        pygame.draw.circle(screen, self.colour, (x, y), self.radius-1)
        
        outer_c = (self.colour[0] - 10, self.colour[1] - 10, self.colour[2] - 10)
        pygame.draw.circle(screen, outer_c, (x, y), self.radius, 5) # Outer circle
        
        # Draw the outline of the text
        outline_surface = self.font.render(self.name, True, (0, 0, 0))
        outline_rect = outline_surface.get_rect(center=(x, y))
        offsets = [(1,1), (-1,-1), (-1,1), (1,-1), (0,1), (0,-1), (1,0), (-1,0)]
        for offset_x, offset_y in offsets:
            position = (outline_rect.x + offset_x, outline_rect.y + offset_y)
            screen.blit(outline_surface, position)

        # Draw the body of the text
        label_surface = self.font.render(self.name, True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(x, y))
        screen.blit(label_surface, label_rect.topleft)

        

    
    
    def distance(self, x, y):
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def can_eat_blob(self, blob):
        if self.distance(blob.x, blob.y) < self.radius + blob.radius:
            return True

    def can_eat_player(self, player):
        if self.distance(player.x, player.y) < self.radius and (self.size > player.size * 1.50):
            return True
    
    def eat(self, food):
        self.size += food.size
        self.radius = math.sqrt(self.size / math.pi)
        self.font = pygame.font.SysFont("arial", self.font_size())

    def decay(self):
        if self.size > 50:
            self.size -= 0.1
            self.radius = math.sqrt(self.size / math.pi)
            
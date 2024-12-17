from Player import Player
import math
import pygame

class Bot(Player):
    def __init__(self, x, y, radius, colour, speed, name):
        super().__init__(x, y, radius, colour, speed, name)
        self.size = math.pi * self.radius ** 2

    def move(self, dx, dy, map_size):
        super().move(dx, dy, map_size)
    
    def draw(self, screen, font, x, y):
        pygame.draw.circle(screen, self.colour, (int(x), int(y)), self.radius)

    def can_eat_blob(self, blob):
        return super().can_eat_blob(blob)

    def eat_blob(self, blob):
        super().eat_blob(blob)

    # Code to find blobs - closest blob
    def search_blob(self, blobs):
        closest_blob = blobs[0]
        for blob in blobs:
            distance = super().distance(blob.x, blob.y)
            if distance < super().distance(closest_blob.x, closest_blob.y):
                closest_blob = blob
        return closest_blob
    
    def move_to_blob(self, closest_blob, map_size):
        distance_x = closest_blob.x - self.x
        distance_y = closest_blob.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if distance != 0:
            direction_x = distance_x / distance
            direction_y = distance_y / distance
        
        dx = direction_x * self.speed * (10 / self.radius)
        dy = direction_y * self.speed * (10 / self.radius)
        super().move(dx, dy, map_size)


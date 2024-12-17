from Player import Player
import math

class Bot(Player):
    def __init__(self, x, y, radius, colour, speed, name):
        super().__init__(x, y, radius, colour, speed, name)
        self.size = math.pi * self.radius ** 2

    def move(self, dx, dy):
        self.move(dx, dy)

    def draw(self, screen, font):
        self.draw(screen, font)
    
    def can_eat_blob(self, blob):
        return self.can_eat_blob(blob)

    def eat_blob(self, blob):
        self.eat_blob(blob)

    # Code to find blobs - closest blob
    def search_blob(self, blobs):
        closest_blob = blobs[0]
        for blob in blobs:
            distance = self.distance(blob.x, blob.y)
            if distance < self.distance(closest_blob.x, closest_blob.y):
                closest_blob = blob
        return closest_blob
                


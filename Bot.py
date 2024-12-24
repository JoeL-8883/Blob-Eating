from Player import Player
import math
import random
import time


class Bot(Player):
    def __init__(self, x, y, radius, colour, speed, name, initial_visibility=100):
        super().__init__(x, y, radius, colour, speed, name)
        self.visibility = self.size/4
        self.random_move_time = 2.5 # Move the bot randomly in one direction if nothing visible
        self.time_random_move = 0
        self.dx = 0
        self.dy = 0

    def move(self, dx, dy, map_size):
        super().move(dx, dy, map_size)
    
    def draw(self, screen, x, y):
        super().draw(screen, x, y)

    def can_eat_blob(self, blob):
        return super().can_eat_blob(blob)

    def eat_blob(self, blob):
        super().eat_blob(blob)

    def is_visible(self, object):
        return super().distance(object.x, object.y) < self.visibility
    
    def update_visbiility(self):
        print("Updating visibility")
        return self.radius * 3

    # Code to find blobs - closest blob
    def search_blob(self, blobs):
        closest_blob = None
        for blob in blobs:
            if self.is_visible(blob):
                if closest_blob is None:
                    closest_blob = blob
                else:
                    distance = super().distance(blob.x, blob.y)
                    if distance < super().distance(closest_blob.x, closest_blob.y):
                        closest_blob = blob
        return closest_blob
    
    def move_to_blob(self, closest_blob, map_size):
        if not closest_blob:
            if time.time() - self.time_random_move > self.random_move_time:
                self.time_random_move = time.time()
                self.dx = random.uniform(-1, 1) * super().movement_speed() * 1.25
                self.dy = random.uniform(-1, 1) * super().movement_speed() * 1.25
        else:
            # Get the distance between the bot and the closest blob
            distance_x = closest_blob.x - self.x
            distance_y = closest_blob.y - self.y
            distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

            # Normalise distance to get direction vector
            
            if distance != 0:
                direction_x = distance_x / distance
                direction_y = distance_y / distance
            
            # Velocity vector to move bot towards blob
            self.dx = direction_x * self.speed * (25 / self.radius)
            self.dy = direction_y * self.speed * (25 / self.radius)
    
        super().move(self.dx, self.dy, map_size)



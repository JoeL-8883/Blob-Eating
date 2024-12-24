from Player import Player
import math
import random

class Bot(Player):
    def __init__(self, x, y, radius, colour, speed, name):
        super().__init__(x, y, radius, colour, speed, name)
        self.visibility = self.radius * 3.5 # This is the Euclidean distance from the bot to any object that can be seen

    def move(self, dx, dy, map_size):
        super().move(dx, dy, map_size)
    
    def draw(self, screen, x, y):
        super().draw(screen, x, y)

    def update_visibility(self):
        self.visibility = self.radius * 3.5

    def is_visible(self, object):
        if super().distance(object.x, object.y) > self.visibility:
            return True

    def can_eat_blob(self, blob):
        return super().can_eat_blob(blob)

    def eat_blob(self, blob):
        super().eat_blob(blob)

    # Code to find blobs - closest blob
    def search_blob(self, blobs):
        closest_blob = None
        for blob in blobs:
            # Check if there is a visible blob
            if closest_blob == None:
                if self.is_visible(blob):
                    closest_blob = blob
            else:
                distance = super().distance(blob.x, blob.y)
                if distance < super().distance(closest_blob.x, closest_blob.y) and self.is_visible(blob):
                    closest_blob = blob
        return closest_blob
    
    def move_to_blob(self, closest_blob, map_size):
        # Get the distance between the bot and the closest blob
        distance_x = closest_blob.x - self.x
        distance_y = closest_blob.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        # Normalise distance to get direction vector
        if distance != 0:
            direction_x = distance_x / distance
            direction_y = distance_y / distance
        # If there's no visible blob, then move randomly
        elif closest_blob == None:
            print("No visible blob")
            direction_x = random.randint(-1, 1)
            direction_y = random.randint(-1, 1)
        
        # Velocity vector to move bot towards blob
        dx = direction_x * self.speed * (25 / self.radius)
        dy = direction_y * self.speed * (25 / self.radius)
        print(dx, dy)
        
        super().move(dx, dy, map_size)



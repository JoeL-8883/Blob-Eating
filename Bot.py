from Player import Player
from Clock import Clock
import math
import random
import time


class Bot(Player):
    def __init__(self, x, y, radius, colour, speed, name):
        super().__init__(x, y, radius, colour, speed, name)
        self.visibility = self.size/4
        self.aggression = random.uniform(0.5, 1.5)
        self.random_move_time = 2.5 # Move the bot randomly in one direction if nothing visible
        self.time_random_move = 0
        self.direction_duration = random.uniform(0.5, 3)
        self.dx = 0
        self.dy = 0
        self.smoothing = 0.4 # Higher smoothing means more responsive but more snappy
        self.clock = Clock()

    def move(self, dx, dy, map_size):
        super().move(dx, dy, map_size)
    
    def draw(self, screen, x, y):
        super().draw(screen, x, y)

    def can_eat_blob(self, blob):
        return super().can_eat_blob(blob)

    def eat(self, object):
        self.update_visbiility() # may not actually need this for bots
        super().eat(object)

    def is_visible(self, object):
        return super().distance(object.x, object.y) + object.radius < self.visibility
    
    def update_visbiility(self):
        self.visibility = self.size/4
    
    def search_closest(self, objects):
        closest = None
        for object in objects:
            if object == self: # Prevent the bot from thinking itself is the closest object
                continue
            if self.is_visible(object):
                if closest is None:
                    closest = object
                else:
                    distance = super().distance(object.x, object.y) + object.radius
                    if distance < super().distance(closest.x, closest.y) + closest.radius: 
                        closest = object
        return closest
    
    def move_to(self, closest, map_size):
        # Move the bot in a random direction for a set time
        if not closest:
            if time.time() - self.time_random_move > self.random_move_time:
                self.time_random_move = time.time()
                self.dx = random.uniform(-1, 1) * super().movement_speed() * 1.25
                self.dy = random.uniform(-1, 1) * super().movement_speed() * 1.25
        else:
            # Get the distance between the bot and the closest
            distance_x = closest.x - self.x + closest.radius
            distance_y = closest.y - self.y + closest.radius
            distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

            # Normalise distance to get direction vector
            
            if distance != 0:
                direction_x = distance_x / distance
                direction_y = distance_y / distance
            
            # Velocity vector to move bot towards object
            dx = direction_x * self.speed * (25 / self.radius)
            dy = direction_y * self.speed * (25 / self.radius)

            self.dx = self.dx * (1 - self.smoothing) + dx * self.smoothing
            self.dy = self.dy * (1 - self.smoothing) + dy * self.smoothing

    
        super().move(self.dx, self.dy, map_size)
    
    def move_away(self, closest, map_size):
        #if self.clock.elapsed_time > self.direction_duration: 
        #self.direction_duration = random.uniform(0.5, 3) + self.clock.elapsed_time

        # Get the distance between the bot and the closest
        distance_x = closest.x - self.x + closest.radius
        distance_y = closest.y - self.y + closest.radius
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        # Normalise distance to get direction vector
        if distance != 0:
            direction_x = distance_x / distance
            direction_y = distance_y / distance
            angle = random.uniform(-math.pi/4, math.pi/4)
            rotated_x = (direction_x * math.cos(angle) - 
                    direction_y * math.sin(angle))
            rotated_y = (direction_x * math.sin(angle) + 
                    direction_y * math.cos(angle))


        # Velocity vector to move bot away from object
        dx = self.speed * (25 / self.radius) # * (-rotated_x)
        dy = self.speed * (25 / self.radius) # * (-rotated_y)

        self.dx = self.dx * (1 - self.smoothing) + dx * self.smoothing
        self.dy = self.dy * (1 - self.smoothing) + dy * self.smoothing
        
        super().move(self.dx, self.dy, map_size)

    def can_eat_player(self, player):
        return super().can_eat_player(player)
    
    def should_flee(self, hunter):
        too_large = hunter.size > 6*self.size
        is_smaller = self.size < hunter.size*1.15
        is_too_close = super().distance(hunter.x, hunter.y) + hunter.radius < (self.visibility)
        return too_large and is_smaller and is_too_close
    
    def should_hunt(self, prey):
        is_larger = self.size > prey.size*1.15
        is_close = super().distance(prey.x, prey.y) + prey.radius < (self.visibility/2)*random.uniform(0.8, 2)
        not_too_small = prey.size > self.size/8 * self.aggression
        return is_larger and is_close and not_too_small

    
    



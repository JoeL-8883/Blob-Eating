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
        self.kills = 0

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
                    if distance < super().distance(closest.x, closest.y): 
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
            # Calculate direction to target center
            distance_x = closest.x - self.x
            distance_y = closest.y - self.y
            distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

            if distance != 0:
                # Normalized direction vector
                direction_x = distance_x / distance
                direction_y = distance_y / distance
                
                # Calculate target velocity
                target_dx = direction_x * self.speed * (25 / self.radius)
                target_dy = direction_y * self.speed * (25 / self.radius)
                
                # Apply smoothing
                self.dx = self.dx * (1 - self.smoothing) + target_dx * self.smoothing
                self.dy = self.dy * (1 - self.smoothing) + target_dy * self.smoothing
    
        super().move(self.dx, self.dy, map_size)
    
    def move_away(self, closest, map_size):
       # Get direction away from threat
        distance_x = closest.x - self.x
        distance_y = closest.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if distance != 0:
            # Base escape direction
            escape_x = -(distance_x / distance)
            escape_y = -(distance_y / distance)
            
            # Calculate boundary repulsion
            edge_weight = 0.5  # Adjust strength of boundary avoidance
            boundary_x = 0
            boundary_y = 0
            
            # Left/Right boundaries
            if self.x < self.radius * 3:
                boundary_x = 1  # Push right
            elif self.x > map_size - self.radius * 3:
                boundary_x = -1  # Push left
                
            # Top/Bottom boundaries
            if self.y < self.radius * 3:
                boundary_y = 1  # Push down
            elif self.y > map_size - self.radius * 3:
                boundary_y = -1  # Push up

            # Combine escape and boundary vectors
            direction_x = escape_x + boundary_x * edge_weight
            direction_y = escape_y + boundary_y * edge_weight
            
            # Normalize combined direction
            magnitude = math.sqrt(direction_x**2 + direction_y**2)
            if magnitude != 0:
                direction_x /= magnitude
                direction_y /= magnitude

            # Apply random rotation
            angle = random.uniform(-math.pi/6, math.pi/6)
            rotated_x = (direction_x * math.cos(angle) - 
                        direction_y * math.sin(angle))
            rotated_y = (direction_x * math.sin(angle) + 
                        direction_y * math.cos(angle))

            # Calculate velocity
            dx = rotated_x * self.speed * (25 / self.radius)
            dy = rotated_y * self.speed * (25 / self.radius)

            # Apply smoothing
            self.dx = self.dx * (1 - self.smoothing) + dx * self.smoothing
            self.dy = self.dy * (1 - self.smoothing) + dy * self.smoothing

        super().move(self.dx, self.dy, map_size)            

    def can_eat_player(self, player):
        return super().can_eat_player(player)
    
    def should_flee(self, hunter):
        not_too_large = hunter.size < 12*self.size
        is_smaller = self.size*1.2 < hunter.size
        is_too_close = super().distance(hunter.x, hunter.y) + hunter.radius + self.radius < (self.visibility/2.1)
        return not_too_large and is_smaller and is_too_close
    
    def should_hunt(self, prey):
        is_larger = self.size > prey.size*1.15
        is_close = super().distance(prey.x, prey.y) + prey.radius + self.radius < (self.visibility/3.5)
        not_too_small = prey.size > self.size/6.5 * self.aggression
        return is_larger and is_close and not_too_small

    
    



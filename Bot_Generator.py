import random
import colours
from Bot import Bot

class Bot_Generator:
    def __init__(self, num_bots, radius, speed, map_size, respawn=False):
        self.num_bots = num_bots
        self.bots = []
        self.respawn = respawn
        self.map_size = map_size
        self.radius = radius
        self.speed = speed

        try:
            with open("names.txt", "r") as f:
                self.names = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print("names.txt not found")
            self.names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivy", "Jack", "Karl", "Lily", "Mia", "Nina", "Oscar", "Penny", "Quinn", "Riley", "Sara", "Tom", "Uma", "Vera", "Wendy", "Xander", "Yara", "Zara"]  
        
        self.generate_bots(radius, speed, map_size)

    def __getitem__(self, index):
        return self.bots[index]
    
    def get_bots(self):
        return self
            
    '''Generate the bots in random positions'''
    def generate_bots(self, radius, speed, map_size):
        for _ in range(self.num_bots):
            bot_x = random.uniform(0, map_size)
            bot_y = random.uniform(0, map_size)
            colour = colours.player()

            # Choose a random name
            if len(self.names) == 0:
                name = 'Rob'
            else:
                name = random.choice(self.names)
                self.names.remove(name)
                
            bot = Bot(bot_x, bot_y, radius, colour, speed, name)
            self.bots.append(bot)
    
    def kill_bot(self, bot):
        self.bots.remove(bot)
        self.num_bots -= 1

        if self.respawn:
            bot = Bot(random.uniform(0, self.map_size), random.uniform(0, self.map_size), self.radius, bot.colour, self.speed, bot.name)
            self.bots.append(bot)
            self.num_bots = len(self.bots)

        
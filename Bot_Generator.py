import random
import colours
from Bot import Bot

class Bot_Generator:
    def __init__(self, num_bots, radius, speed, map_size):
        self.num_bots = num_bots
        self.bots = []
        self.generate_bots(radius, speed, map_size)
    
    def __getitem__(self, index):
        return self.bots[index]

    '''Generate the bots in random positions'''
    def generate_bots(self, radius, speed, map_size):
        for _ in range(self.num_bots):
            bot_x = random.uniform(0, map_size)
            bot_y = random.uniform(0, map_size)
            colour = colours.player()
            bot = Bot(bot_x, bot_y, radius, colour, speed, "Ridley")
            self.bots.append(bot)
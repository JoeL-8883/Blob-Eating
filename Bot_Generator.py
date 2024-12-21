import random
import colours
from Bot import Bot

class Bot_Generator:
    def __init__(self, num_bots, radius, speed, map_size, respawn = False):
        self.num_bots = num_bots
        self.bots = []
        self.generate_bots(radius, speed, map_size)
        self.respawn = respawn

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
            bot = Bot(bot_x, bot_y, radius, colour, speed, "Ridley")
            self.bots.append(bot)
    
    def kill_bot(self, bot):
        self.bots.remove(bot)
        self.num_bots -= 1

        if self.respawn:
            bot = Bot(random.uniform(0, self.map_size), random.uniform(0, self.map_size), bot.radius, bot.colour, bot.speed, bot.name)
            self.bots.append(bot)
            self.num_bots = len(self.bots)

        
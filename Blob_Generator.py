import colours
import random
from Blob import Blob
import math


class Blob_Generator:
    def __init__(self, map_size, initial, rate=1):
        self.blobs = []
        self.limit = initial
        self.map_size = map_size
        self.create(map_size, initial)
        self.rate = rate

    def __getitem__(self, index):
        return self.blobs[index]

    def get_blobs(self):
        return self.blobs

    # Create blob objects
    def create(self, map_size, n):
        def normalised_distance_to_centre(x, y):
            centre = map_size / 2
            distance_to_centre = (x - centre) ** 2 + (y - centre) ** 2
            max_distance = (math.sqrt(2) * (map_size / 2)) 
            return (distance_to_centre / max_distance)
            
        for _ in range(n):
            x = random.uniform(0, map_size)
            y = random.uniform(0, map_size)
            r = random.uniform(4, 10)
            c = colours.blob()

            lifetime = 5000 * random.uniform(10, 20) / normalised_distance_to_centre(x, y)

            blob = Blob(x, y, r, c, lifetime)
            self.blobs.append(blob)

    # Generate a random number of blobs after blobs have been eaten
    def add_blobs(self):
        if len(self.blobs) < self.limit:
            n = random.randint(0, 2) * self.rate
            self.create(self.map_size, n)

    def draw_blobs(self):
        for blob in self.blobs:
            blob.draw()
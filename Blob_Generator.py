import colours
import random
from Blob import Blob


class Blob_Generator:
    def __init__(self, map_size, initial):
        self.blobs = []
        self.limit = initial
        self.map_size = map_size
        self.create(map_size, initial)

    def __getitem__(self, index):
        return self.blobs[index]

    def get_blobs(self):
        return self.blobs

    # Create blob objects
    def create(self, map_size, n):
        for _ in range(n):
            x = random.uniform(0, map_size)
            y = random.uniform(0, map_size)
            r = random.uniform(4, 10)
            c = colours.blob()
            blob = Blob(x, y, r, c)
            self.blobs.append(blob)

    # Generate a random number of blobs after blobs have been eaten
    def add_blobs(self):
        if len(self.blobs) < self.limit:
            n = random.randint(1, 3)
            self.create(self.map_size, n)

    def draw_blobs(self):
        for blob in self.blobs:
            blob.draw()
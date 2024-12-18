import random

def player():
    return (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255))

def blob():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

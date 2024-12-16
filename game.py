import pygame
import random
import math
from Player import Player
from Blob import Blob

# Initialize Pygame
pygame.init()
pygame.font.init()

# Screen / viewport dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI Blob Eating")

# Clock for frame rate
clock = pygame.time.Clock()

# Map size (larger than the viewport)
MAP_SIZE = 3000

# Constants for player attributes
PLAYER_RADIUS = 20
PLAYER_COLOR = (255, 255, 255)  # white
PLAYER_SPEED = 3.0
PLAYER_LABEL = "Joe"

# Create a player
player_x = MAP_SIZE / 2
player_y = MAP_SIZE / 2
plr = Player(player_x, player_y, PLAYER_RADIUS, PLAYER_COLOR, PLAYER_SPEED, PLAYER_LABEL)

# Generate collectible blobs
BLOB_COUNT = 200
blobs = []
for _ in range(BLOB_COUNT):
    # Create a blob
    bx = random.uniform(0, MAP_SIZE)
    by = random.uniform(0, MAP_SIZE)
    br = random.uniform(4, 10)
    bc = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    blob = Blob(bx, by, br, bc)
    blobs.append(blob)

# Movement keys state
move_up = move_down = move_left = move_right = False

running = True
while running:
    clock.tick(60)  # Target 60 fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP):
                move_up = True
            if event.key in (pygame.K_s, pygame.K_DOWN):
                move_down = True
            if event.key in (pygame.K_a, pygame.K_LEFT):
                move_left = True
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                move_right = True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_UP):
                move_up = False
            if event.key in (pygame.K_s, pygame.K_DOWN):
                move_down = False
            if event.key in (pygame.K_a, pygame.K_LEFT):
                move_left = False
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                move_right = False

    # Move the player
    dx = dy = 0
    if move_up:
        dy -= plr.speed * (20 / plr.radius)  # Slow down as player grows
    if move_down:
        dy += plr.speed * (20 / plr.radius)
    if move_left:
        dx -= plr.speed * (20 / plr.radius)
    if move_right:
        dx += plr.speed * (20 / plr.radius)

    # Update player position
    plr.move(dx, dy)

    # Constrain player to map boundaries
    if plr.x < plr.radius:
        plr.x = plr.radius
    if plr.y < plr.radius:
        plr.y = plr.radius
    if plr.x > MAP_SIZE - plr.radius:
        plr.x = MAP_SIZE - plr.radius
    if plr.y > MAP_SIZE - plr.radius:
        plr.y = MAP_SIZE - plr.radius

    # Check collision with blobs
    # Distance-based collision for circles
    to_remove = []
    for i, blob in enumerate(blobs):
        if plr.can_eat_blob(blob):
            plr.eat_blob(blob)
            to_remove.append(i)

    # Remove eaten blobs - note that blobs are removed this way to maintain indexing
    for i in reversed(to_remove):
        del blobs[i]

    # DRAWING
    screen.fill((50, 50, 50))  # background

    # Calculate offsets to center player
    offset_x = SCREEN_WIDTH / 2 - plr.x
    offset_y = SCREEN_HEIGHT / 2 - plr.y

    # Draw map boundary (optional visualization)
    # Just draw a large rectangle representing the map boundary
    boundary_color = (100, 100, 100)
    pygame.draw.rect(screen, boundary_color, (offset_x, offset_y, MAP_SIZE, MAP_SIZE), 2)

    # Draw blobs
    for blob in blobs:
        pygame.draw.circle(screen, blob.colour, (int(blob.x + offset_x), int(blob.y + offset_y)), int(blob.radius))

    # Draw player
    pygame.draw.circle(screen, plr.colour, (int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2)), int(plr.radius))

    # Update display
    pygame.display.flip()

print("Quitting...")
pygame.quit()
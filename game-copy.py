import pygame
import random
import math

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

# Player attributes
player_x = MAP_SIZE / 2
player_y = MAP_SIZE / 2
player_radius = 20
player_color = (255, 255, 255)  # white
player_speed = 3.0
player_label = "Joe"

# Generate collectible blobs
BLOB_COUNT = 200
blobs = []
for _ in range(BLOB_COUNT):
    bx = random.uniform(0, MAP_SIZE)
    by = random.uniform(0, MAP_SIZE)
    br = random.uniform(4, 8)
    bc = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    blobs.append([bx, by, br, bc])

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
        dy -= player_speed * (20 / player_radius)  # Slow down as player grows
    if move_down:
        dy += player_speed * (20 / player_radius)
    if move_left:
        dx -= player_speed * (20 / player_radius)
    if move_right:
        dx += player_speed * (20 / player_radius)

    # Update player position
    player_x += dx
    player_y += dy

    # Constrain player to map boundaries
    if player_x < player_radius:
        player_x = player_radius
    if player_y < player_radius:
        player_y = player_radius
    if player_x > MAP_SIZE - player_radius:
        player_x = MAP_SIZE - player_radius
    if player_y > MAP_SIZE - player_radius:
        player_y = MAP_SIZE - player_radius

    # Check collision with blobs
    # Distance-based collision for circles
    to_remove = []
    for i, blob in enumerate(blobs):
        bx, by, br, bc = blob
        dist = math.sqrt((player_x - bx)**2 + (player_y - by)**2)
        if dist < player_radius + br:
            # Eat the blob
            # Increase player's radius based on area
            player_area = math.pi * (player_radius**2)
            blob_area = math.pi * (br**2)
            new_area = player_area + blob_area
            player_radius = math.sqrt(new_area / math.pi)
            to_remove.append(i)

    # Remove eaten blobs
    for i in reversed(to_remove):
        del blobs[i]

    # DRAWING
    screen.fill((50, 50, 50))  # background

    # Calculate offsets to center player
    offset_x = SCREEN_WIDTH / 2 - player_x
    offset_y = SCREEN_HEIGHT / 2 - player_y

    # Draw map boundary (optional visualization)
    # Just draw a large rectangle representing the map boundary
    boundary_color = (100, 100, 100)
    pygame.draw.rect(screen, boundary_color, (offset_x, offset_y, MAP_SIZE, MAP_SIZE), 2)

    # Draw blobs
    for (bx, by, br, bc) in blobs:
        pygame.draw.circle(screen, bc, (int(bx + offset_x), int(by + offset_y)), int(br))

    # Draw player
    pygame.draw.circle(screen, player_color, (int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2)), int(player_radius))

    # Update display
    pygame.display.flip()

pygame.quit()
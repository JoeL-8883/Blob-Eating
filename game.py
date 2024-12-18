import pygame
import random
import colours
from Player import Player
from Blob import Blob
from Bot import Bot
from Bot_Generator import Bot_Generator
from Blob_Generator import Blob_Generator


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
PLAYER_RADIUS = 30
PLAYER_COLOR = colours.player()
PLAYER_SPEED = 7.5
PLAYER_LABEL = "Joe"

# Create a player
player_x = MAP_SIZE / 2
player_y = MAP_SIZE / 2
plr = Player(player_x, player_y, PLAYER_RADIUS, PLAYER_COLOR, PLAYER_SPEED, PLAYER_LABEL)

# Create bots
bots = Bot_Generator(10, PLAYER_RADIUS, PLAYER_SPEED, MAP_SIZE)

# Generate collectible blobs -- will move to the while loop eventually
BLOB_COUNT = 800 # Maximum number of blobs
EATEN = 0
blobs = Blob_Generator(MAP_SIZE, BLOB_COUNT)

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

    blobs_list = blobs.get_blobs() # Find a way to make this better?


    # Move the player
    dx = dy = 0
    if move_up:
        dy -= plr.speed * (25 / plr.radius)  # Slow down as player grows
    if move_down:
        dy += plr.speed * (25 / plr.radius)
    if move_left:
        dx -= plr.speed * (25 / plr.radius)
    if move_right:
        dx += plr.speed * (25 / plr.radius)

    # Update player position
    plr.move(dx, dy, MAP_SIZE)

    # Bot movement
    closest_blob = bots[0].search_blob(blobs_list)
    for bot in bots:
        closest_blob = bot.search_blob(blobs_list)
        bot.move_to_blob(closest_blob, MAP_SIZE)

    # Check if blob has been eaten already for optimisation
    eaten_blobs = []
    for i, blob in enumerate(blobs_list):
        if i in eaten_blobs:
            continue
        elif plr.can_eat_blob(blob):
            plr.eat(blob)
            EATEN += 1
            eaten_blobs.append(i)
        
        # Check if bots can eat blob
        for bot in bots:
            if i in eaten_blobs:
                break
            elif bot.can_eat_blob(blob):
                bot.eat(blob)
                EATEN += 1
                eaten_blobs.append(i)

    for bot in bots:
        if plr.can_eat_player(bot):
            plr.eat(bot)
            print("Player has eaten a bot")
            bots.kill_bot(bot)
            break

    if len(eaten_blobs) > 0:
        # Remove eaten blobs
        while len(eaten_blobs) > 0:
            i = eaten_blobs.pop()
            blobs_list.pop(i)

    # Add new blobs
    blobs.add_blobs()  

    # Calculate offsets to center player
    offset_x = SCREEN_WIDTH / 2 - plr.x
    offset_y = SCREEN_HEIGHT / 2 - plr.y

    # DRAWING
    screen.fill((240, 240, 240))  # background

    grid_color = (220, 220, 220)  # Light gray
    grid_spacing = 100  # Space between grid lines

    # Vertical lines
    for x in range(0, MAP_SIZE, grid_spacing):
        pygame.draw.line(screen, grid_color, 
                        (x + offset_x, offset_y), 
                        (x + offset_x, MAP_SIZE + offset_y))

    # Horizontal lines
    for y in range(0, MAP_SIZE, grid_spacing):
        pygame.draw.line(screen, grid_color,
                        (offset_x, y + offset_y),
                        (MAP_SIZE + offset_x, y + offset_y))



    # Draw map boundary (optional visualization)
    # Just draw a large rectangle representing the map boundary
    boundary_color = (100, 100, 100)
    pygame.draw.rect(screen, boundary_color, (offset_x, offset_y, MAP_SIZE, MAP_SIZE), 2)

    # Draw blobs
    for blob in blobs_list:
        pygame.draw.circle(screen, blob.colour, (blob.x + offset_x, blob.y + offset_y), int(blob.radius))
    
    # Draw player
    #pygame.draw.circle(screen, plr.colour, (int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2)), int(plr.radius))
    plr.draw(screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    
    for bot in bots:
        bot.draw(screen, bot.x + offset_x, bot.y + offset_y)
    
    
    # Update display
    pygame.display.flip()

print("Quitting...")
pygame.quit()
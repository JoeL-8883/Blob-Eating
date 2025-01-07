import pygame
import random
import colours
import keys
from Player import Player
from Blob import Blob
from Bot import Bot
from Bot_Generator import Bot_Generator
from Blob_Generator import Blob_Generator
from Clock import Clock


# Initialize Pygame
pygame.init()
pygame.font.init()

# Screen / viewport dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
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
player_x = random.uniform(0, MAP_SIZE)
player_y = random.uniform(0, MAP_SIZE)
player = Player(player_x, player_y, PLAYER_RADIUS, PLAYER_COLOR, PLAYER_SPEED, PLAYER_LABEL)

# Create bots
NUM_BOTS = 20
bots = Bot_Generator(NUM_BOTS, PLAYER_RADIUS, PLAYER_SPEED, MAP_SIZE, True, player)

# Generate collectible blobs -- will move to the while loop eventually
BLOB_COUNT = 300 # Maximum number of blobs
EATEN = 0
EATEN_PLAYERS = 0
blobs = Blob_Generator(MAP_SIZE, BLOB_COUNT)

# Movement keys state
move_up = move_down = move_left = move_right = False

running = True
game_clock = Clock()
while running:
    game_clock.update()
    clock.tick(60)  # Target 60 fps

    # Handles key presses
    running, move_up, move_down, move_left, move_right = keys.keys(pygame, running, move_up, move_down, move_left, move_right)

    blobs_list = blobs.get_blobs() # Find a way to make this better?

    # Calculate speed based off which key is pressed
    dx, dy = player.velocity(move_up, move_down, move_left, move_right)

    # Update player position
    player.move(dx, dy, MAP_SIZE)

    # Bot hunting
    '''To get this working, I'll need to design and implement the following 
        - intelligence/aggression system
        - correct movement based on surroundings
        - fix glitchy movement
        - eventually I'll induce some form of utility where the bots make decisions based on what they can see, i.e. hunt for larger blobs
    '''
    for bot in bots:
        if bot == player:
            continue
        
        closest_blob = bot.search_closest(blobs_list)
        closest_bot = bot.search_closest(bots.get_bots())

        if closest_bot:
            if bot.should_flee(closest_bot):
                bot.move_away(closest_bot, MAP_SIZE)
            elif bot.should_hunt(closest_bot):
                bot.move_to(closest_bot, MAP_SIZE)
            else:
                bot.move_to(closest_blob, MAP_SIZE)        
        else:
            bot.move_to(closest_blob, MAP_SIZE)

      
        for eat_bot in bots:
            if eat_bot == bot:
                continue
            if bot.can_eat_player(eat_bot):
                bot.eat(eat_bot)
                bots.kill_bot(eat_bot)
                EATEN_PLAYERS += 1
                print(bot.name, " ate " , eat_bot.name)


    # Check if blob has been eaten already for optimisation
    eaten_blobs = []
    for i, blob in enumerate(blobs_list):
        if i in eaten_blobs:
            continue
        elif player.can_eat_blob(blob):
            player.eat(blob)
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

        # If the blob should die kill it
        if blob.die():
            eaten_blobs.append(i)
        
    if len(eaten_blobs) > 0:
        # Remove eaten blobs
        while len(eaten_blobs) > 0:
            i = eaten_blobs.pop()
            blobs_list.pop(i)
    
    for bot in bots:
        if player.can_eat_player(bot):
            player.eat(bot)
            bots.kill_bot(bot)
            EATEN_PLAYERS += 1 
            break

    # Add new blobs
    blobs.add_blobs()  

    # Decay players size
    player.decay()
    for bot in bots.get_bots():
        bot.decay()

    # Calculate offsets to center player
    offset_x = SCREEN_WIDTH / 2 - player.x
    offset_y = SCREEN_HEIGHT / 2 - player.y

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
    player.draw(screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    
    for bot in bots:
        bot.draw(screen, bot.x + offset_x, bot.y + offset_y)
    
    # Update display
    pygame.display.flip()

print("Quitting...")
pygame.quit()
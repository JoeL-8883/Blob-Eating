import pygame

class Leaderboard:
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 16)
        self.scores = []  # List of (name, kills) tuples
        self.max_display = 5  # Number of scores to show
        
    def update(self, player, bots):
        # Clear previous scores
        self.scores = []
        
        # Add player score if playing
        if player:
            self.scores.append((player.name, player.size))
            
        # Add bot scores
        for bot in bots:
            self.scores.append((bot.name, bot.size))
            
        # Sort by size descending 
        self.scores.sort(key=lambda x: x[1], reverse=True)
        
    def draw(self, screen):
        # Draw background
        padding = 15
        width = 150
        height = (self.max_display + 1) * 20
        background = pygame.Surface((width, height), pygame.SRCALPHA)
        background.fill((200, 200, 200, 100))
        screen.blit(background, (padding, padding))

        # Draw scores
        y = padding + 25
        for i, (name, kills) in enumerate(self.scores[:self.max_display]):
            text = self.font.render(f"{i+1}. {name}", True, (0, 0, 0))
            screen.blit(text, (padding + 5, y + - 10))
            y += 20
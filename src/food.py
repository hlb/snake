import random
import pygame
from pygame_emojis import load_emoji
from .constants import GRID_WIDTH, GRID_HEIGHT, GRID_SIZE

class Food:
    def __init__(self, obstacles):
        self.position = (0, 0)
        self.obstacles = obstacles
        self.food_emojis = ['🍕', '🍇', '🍪', '🍓', '🍎', '🍮', '🍜']
        self.emoji = random.choice(self.food_emojis)
        # Load the emoji surface
        self.emoji_surface = load_emoji(self.emoji, (GRID_SIZE - 4, GRID_SIZE - 4))
        self.randomize_position()

    def randomize_position(self):
        """Randomize the food position, ensuring it's not on an obstacle."""
        while True:
            self.position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            # Make sure food doesn't spawn on an obstacle
            if self.position not in self.obstacles.positions:
                break
        # Randomly change emoji
        self.emoji = random.choice(self.food_emojis)
        self.emoji_surface = load_emoji(self.emoji, (GRID_SIZE - 4, GRID_SIZE - 4))

    def render(self, screen):
        """Render the food emoji on the screen."""
        x = self.position[0] * GRID_SIZE + 2
        y = self.position[1] * GRID_SIZE + 2
        screen.blit(self.emoji_surface, (x, y))

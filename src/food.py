import random
import pygame
from pygame_emojis import load_emoji
from .constants import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    NORMAL_FOOD_COLOR, GOLDEN_APPLE_COLOR, SPEED_FRUIT_COLOR,
    FOOD_TYPES
)

class Food:
    def __init__(self, obstacles):
        """Initialize food with random position and type."""
        self.obstacles = obstacles
        self.position = (0, 0)
        # Define emoji for each food type
        self.food_emojis = {
            'normal': ['🍕', '🍇', '🍪', '🍓'],
            'golden': ['🌟', '⭐', '🌞'],
            'speed': ['⚡', '🚀', '💨']
        }
        self._initialize_food()
    
    def _initialize_food(self):
        """Initialize food with random position and type."""
        self.randomize_position()
        self._set_random_type()
    
    def _set_random_type(self):
        """Set a random food type based on probabilities."""
        # 70% normal, 15% golden, 15% speed
        rand = random.random()
        if rand < 0.70:
            self.type = 'normal'
            self.color = NORMAL_FOOD_COLOR
        elif rand < 0.85:
            self.type = 'golden'
            self.color = GOLDEN_APPLE_COLOR
        else:
            self.type = 'speed'
            self.color = SPEED_FRUIT_COLOR
        
        # Get effect properties and set emoji
        self.properties = FOOD_TYPES[self.type]
        self.emoji = random.choice(self.food_emojis[self.type])
        self.emoji_surface = load_emoji(self.emoji, (GRID_SIZE - 4, GRID_SIZE - 4))
    
    def randomize_position(self):
        """Randomize food position, avoiding obstacles."""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            pos = (x, y)
            if pos not in self.obstacles.positions:
                self.position = pos
                self._set_random_type()
                break
    
    def render(self, screen):
        """Render food on screen with both color and emoji."""
        # Draw colored background
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE + 2,
            self.position[1] * GRID_SIZE + 2,
            GRID_SIZE - 4,
            GRID_SIZE - 4
        )
        pygame.draw.rect(screen, self.color, rect, border_radius=10)
        
        # Draw emoji
        x = self.position[0] * GRID_SIZE + 2
        y = self.position[1] * GRID_SIZE + 2
        screen.blit(self.emoji_surface, (x, y))

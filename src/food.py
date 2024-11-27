import random
import pygame
from pygame_emojis import load_emoji
from .constants import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    NORMAL_FOOD_COLOR, GOLDEN_APPLE_COLOR, SPEED_FRUIT_COLOR,
    FOOD_TYPES
)

class FoodItem:
    """Represents a single food item in the game."""
    def __init__(self, position, type_name, color, properties, emoji, emoji_surface):
        self.position = position
        self.type = type_name
        self.color = color
        self.properties = properties
        self.emoji = emoji
        self.emoji_surface = emoji_surface

    def render(self, screen):
        """Render food item on screen with both color and emoji."""
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

class Food:
    def __init__(self, obstacles, max_foods=3):
        """Initialize food manager with multiple food items."""
        self.obstacles = obstacles
        self.max_foods = max_foods
        self.foods = []  # List to store multiple food items
        
        # Define emoji for each food type
        self.food_emojis = {
            'normal': ['🍕', '🍇', '🍪', '🍓'],
            'golden': ['🌟', '⭐', '🌞'],
            'speed': ['⚡', '🚀', '💨']
        }
        
        # Initialize food items
        self._ensure_minimum_food()
    
    def _create_food_item(self, position=None):
        """Create a new food item with random type at given or random position."""
        if position is None:
            position = self._get_random_position()
        
        # Set random type based on probabilities
        rand = random.random()
        if rand < 0.70:
            type_name = 'normal'
            color = NORMAL_FOOD_COLOR
        elif rand < 0.85:
            type_name = 'golden'
            color = GOLDEN_APPLE_COLOR
        else:
            type_name = 'speed'
            color = SPEED_FRUIT_COLOR
        
        # Get effect properties and set emoji
        properties = FOOD_TYPES[type_name]
        emoji = random.choice(self.food_emojis[type_name])
        emoji_surface = load_emoji(emoji, (GRID_SIZE - 4, GRID_SIZE - 4))
        
        return FoodItem(position, type_name, color, properties, emoji, emoji_surface)
    
    def _get_random_position(self):
        """Get a random position that doesn't overlap with obstacles, other food, or previous positions."""
        attempts = 0
        max_attempts = 100  # Prevent infinite loop
        previous_positions = {food.position for food in self.foods}
        
        while attempts < max_attempts:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            pos = (x, y)
            
            # Check if position is valid and not in previous positions
            if (pos not in self.obstacles.positions and 
                pos not in previous_positions):
                return pos
            attempts += 1
        
        # If we couldn't find a new position after max attempts,
        # just return any valid position
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            pos = (x, y)
            if pos not in self.obstacles.positions:
                return pos
    
    def _ensure_minimum_food(self):
        """Ensure there is always at least one food item."""
        while len(self.foods) < self.max_foods:
            self.foods.append(self._create_food_item())
    
    def remove_food(self, position):
        """Remove food at given position and return its properties."""
        for i, food in enumerate(self.foods):
            if food.position == position:
                properties = food.properties
                self.foods.pop(i)
                self.foods.append(self._create_food_item())
                return properties
        return None
    
    @property
    def positions(self):
        """Get all food positions."""
        return [food.position for food in self.foods]
    
    def render(self, screen):
        """Render all food items."""
        for food in self.foods:
            food.render(screen)

import os
import pygame

# Color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (40, 44, 52)
GRID_COLOR = (50, 54, 62)
SNAKE_COLOR = (152, 195, 121)
FOOD_COLOR = (224, 108, 117)
SCORE_COLOR = (229, 192, 123)
GAME_OVER_COLOR = (224, 108, 117)
OBSTACLE_COLOR = (97, 175, 239)

# Game settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 40
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
INITIAL_SPEED = 6  # Initial speed
SPEED_INCREMENT = 1  # Speed increase per 10 points
OBSTACLE_COUNT = 3

# Direction constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def get_font(size):
    # macOS system font paths
    system_fonts = [
        '/System/Library/Fonts/PingFang.ttc',  # PingFang
        '/System/Library/Fonts/STHeiti Light.ttc',  # Heiti
        '/System/Library/Fonts/Hiragino Sans GB.ttc'  # Hiragino
    ]
    
    # Try to load system fonts
    for font_path in system_fonts:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except:
                continue
    
    # If no Chinese fonts found, use default font
    return pygame.font.Font(None, size)

def draw_rounded_rect(surface, color, rect, radius):
    """Draw a rounded rectangle"""
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_grid(screen):
    """Draw background grid"""
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

import unittest
import pygame
from src import (
    Snake, Food, Obstacle,
    GRID_WIDTH, GRID_HEIGHT, UP, DOWN, LEFT, RIGHT
)

class SnakeGameTest(unittest.TestCase):
    """Base test class for snake game tests with common setup and teardown."""
    
    @classmethod
    def setUpClass(cls):
        """Set up class-level resources."""
        pygame.init()
        pygame.display.set_mode((800, 600))
    
    @classmethod
    def tearDownClass(cls):
        """Clean up class-level resources."""
        pygame.quit()
    
    def setUp(self):
        """Set up test environment before each test."""
        self.screen = pygame.display.get_surface()
        self.obstacles = Obstacle()
        self.snake = Snake()
        self.food = Food(self.obstacles)

    def assert_position_in_grid(self, position):
        """Assert that a position is within the game grid."""
        self.assertTrue(0 <= position[0] < GRID_WIDTH)
        self.assertTrue(0 <= position[1] < GRID_HEIGHT)

    def assert_valid_direction(self, direction):
        """Assert that a direction is valid."""
        self.assertIn(direction, [UP, DOWN, LEFT, RIGHT])

    def create_test_snake_at(self, position, direction=None):
        """Create a snake at a specific position with optional direction."""
        direction = direction or RIGHT
        dx, dy = direction
        # Create snake body behind the head based on direction
        positions = [position]
        for i in range(1, self.snake.length):
            positions.append((
                (position[0] - dx * i) % GRID_WIDTH,
                (position[1] - dy * i) % GRID_HEIGHT
            ))
        self.snake.positions = positions
        self.snake.direction = direction
        return self.snake

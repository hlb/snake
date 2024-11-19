import unittest
import pygame
from snake_game import Snake, Food, Obstacle, GRID_WIDTH, GRID_HEIGHT, GRID_SIZE, UP, DOWN, LEFT, RIGHT

class TestSnakeGame(unittest.TestCase):
    def setUp(self):
        # Initialize Pygame as it's required for the game
        pygame.init()
        # Create a test display surface
        self.screen = pygame.display.set_mode((800, 600))
        # Create obstacles instance for testing
        self.obstacles = Obstacle()
        
    def test_snake_initial_state(self):
        snake = Snake()
        # Test initial length
        self.assertEqual(len(snake.positions), 3)
        # Test that all positions are within grid
        for pos in snake.positions:
            self.assertTrue(0 <= pos[0] < GRID_WIDTH)
            self.assertTrue(0 <= pos[1] < GRID_HEIGHT)
        # Test initial direction is valid
        self.assertIn(snake.direction, [UP, DOWN, LEFT, RIGHT])
        # Test initial score
        self.assertEqual(snake.score, 0)

    def test_snake_movement(self):
        snake = Snake()
        initial_head = snake.get_head_position()
        snake.direction = RIGHT
        snake.update(self.obstacles)
        new_head = snake.get_head_position()
        # Test horizontal movement
        self.assertEqual(new_head[0], (initial_head[0] + 1) % GRID_WIDTH)
        self.assertEqual(new_head[1], initial_head[1])

    def test_snake_collision_with_self(self):
        snake = Snake()
        # Force snake to collide with itself
        snake.positions = [(6, 5), (5, 5), (4, 5)]  # Snake moving right
        snake.direction = LEFT  # Moving left will cause collision with body
        # Should return True for collision
        self.assertTrue(snake.update(self.obstacles))

    def test_food_initialization(self):
        food = Food(self.obstacles)
        # Test that food position is within grid
        self.assertTrue(0 <= food.position[0] < GRID_WIDTH)
        self.assertTrue(0 <= food.position[1] < GRID_HEIGHT)
        # Test that food has an emoji
        self.assertTrue(hasattr(food, 'emoji'))
        self.assertTrue(hasattr(food, 'emoji_surface'))

    def test_food_randomize_position(self):
        food = Food(self.obstacles)
        initial_pos = food.position
        initial_emoji = food.emoji
        food.randomize_position()
        # Test that either position or emoji has changed
        different_pos = initial_pos != food.position
        different_emoji = initial_emoji != food.emoji
        self.assertTrue(different_pos or different_emoji)

    def test_obstacle_initialization(self):
        obstacles = Obstacle()
        # Test that obstacles are created
        self.assertTrue(len(obstacles.positions) > 0)
        # Test that all obstacles are within grid
        for pos in obstacles.positions:
            self.assertTrue(0 <= pos[0] < GRID_WIDTH)
            self.assertTrue(0 <= pos[1] < GRID_HEIGHT)

    def test_snake_collision_with_obstacle(self):
        snake = Snake()
        # Force snake to be at a specific position
        snake.positions = [(5, 5)]
        # Add obstacle at snake's next position
        self.obstacles.positions = {(6, 5)}
        snake.direction = RIGHT
        # Should return True for collision
        self.assertTrue(snake.update(self.obstacles))

    def test_snake_growth(self):
        snake = Snake()
        initial_length = len(snake.positions)
        # Simulate eating food
        snake.score += 1
        snake.update(self.obstacles)
        # Test that snake grew
        self.assertEqual(len(snake.positions), initial_length + 1)

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()

import pygame
from tests.test_base import SnakeGameTest
from src import Food

class TestFood(SnakeGameTest):
    """Unit tests for Food class functionality."""

    def test_food_initialization(self):
        """Test food initialization and properties."""
        self.assertEqual(len(self.food.foods), 3)
        for food_item in self.food.foods:
            self.assert_position_in_grid(food_item.position)
            self.assertNotIn(food_item.position, self.obstacles.positions)
            self.assertIn(food_item.type, ['normal', 'golden', 'speed'])
            self.assertIn('points', food_item.properties)

    def test_food_effects(self):
        """Test different food effects on snake."""
        # Test golden apple effect
        initial_score = self.snake.score
        self.snake.handle_food_effect({'points': 2, 'speed_change': 0, 'duration': 0})
        self.assertEqual(self.snake.score, initial_score + 2)

        # Test speed fruit effect
        initial_speed = self.snake.speed
        self.snake.handle_food_effect({'points': 1, 'speed_change': 2, 'duration': 1})
        self.assertEqual(self.snake.speed, initial_speed + 2)
        pygame.time.wait(10)
        self.snake.update(self.obstacles)
        self.assertEqual(self.snake.speed, initial_speed)

    def test_food_position_randomization(self):
        """Test that food positions are properly randomized."""
        # Get initial food positions
        initial_positions = {food.position for food in self.food.foods}
        
        # Force food regeneration
        new_food = Food(self.obstacles)
        
        # Get new positions
        new_positions = {food.position for food in new_food.foods}
        
        # Verify that at least some positions are different
        self.assertTrue(initial_positions != new_positions)

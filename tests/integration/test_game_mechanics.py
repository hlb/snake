import pygame
from tests.base_test import SnakeGameTest
from src import UP, DOWN, LEFT, RIGHT, Snake
from snake_game import handle_direction_change, update_game_state

class TestGameMechanics(SnakeGameTest):
    """Integration tests for game mechanics."""

    def test_game_reset(self):
        """Test game reset functionality."""
        # Modify game state
        self.snake.score = 100
        self.snake.positions = [(1, 1)]
        
        # Reset game by creating new snake
        self.snake = Snake()
        
        # Verify reset state
        self.assertEqual(self.snake.score, 0)
        self.assertEqual(len(self.snake.positions), 3)
        self.assert_valid_direction(self.snake.direction)

    def test_direction_change(self):
        """Test direction change handling."""
        from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
        
        # Test valid direction changes
        self.snake.direction = RIGHT
        handle_direction_change(K_UP, self.snake)
        self.assertEqual(self.snake.direction, UP)
        
        handle_direction_change(K_DOWN, self.snake)
        self.assertEqual(self.snake.direction, UP)  # Should not change to opposite direction

    def test_game_state_update(self):
        """Test game state updates."""
        # Place food in snake's path
        self.snake = self.create_test_snake_at((5, 5), RIGHT)
        self.food.foods[0].position = (6, 5)
        
        # Update game state
        initial_score = self.snake.score
        update_game_state(self.snake, self.obstacles, self.food)
        
        # Verify food collection
        self.assertTrue(self.snake.score > initial_score)

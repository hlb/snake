import pygame
from tests.base_test import SnakeGameTest
from snake_game import show_start_menu, render_game

class TestUI(SnakeGameTest):
    """Integration tests for UI components."""

    def test_start_menu_rendering(self):
        """Test start menu rendering."""
        show_start_menu(self.screen)
        pygame.display.flip()

    def test_game_rendering(self):
        """Test game screen rendering."""
        render_game(self.screen, self.snake, self.food, self.obstacles, False)
        pygame.display.flip()

    def test_score_display(self):
        """Test score display functionality."""
        initial_score = self.snake.score
        self.snake.score += 10
        render_game(self.screen, self.snake, self.food, self.obstacles, False)
        pygame.display.flip()
        self.assertEqual(self.snake.score, initial_score + 10)

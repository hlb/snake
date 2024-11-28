import unittest
import os
import pygame
from datetime import datetime
from src.ui import Screenshot, GameRenderer
from src import WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND


class TestScreenshot(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screenshot = Screenshot()

    def tearDown(self):
        """Clean up after each test."""
        pygame.quit()
        # Clean up any screenshots
        if os.path.exists(self.screenshot.directory):
            for file in os.listdir(self.screenshot.directory):
                os.remove(os.path.join(self.screenshot.directory, file))
            os.rmdir(self.screenshot.directory)

    def test_screenshot_directory_creation(self):
        """Test screenshot directory is created."""
        self.assertTrue(os.path.exists(self.screenshot.directory))

    def test_screenshot_scheduling(self):
        """Test screenshot scheduling mechanism."""
        self.assertFalse(self.screenshot.pending)

        self.screenshot.schedule()
        self.assertTrue(self.screenshot.pending)
        self.assertGreater(self.screenshot.scheduled_time, pygame.time.get_ticks())

    def test_screenshot_capture(self):
        """Test screenshot capture functionality."""
        # Clean any existing screenshots first
        for file in os.listdir(self.screenshot.directory):
            os.remove(os.path.join(self.screenshot.directory, file))

        # Schedule and force immediate capture
        self.screenshot.schedule()
        self.screenshot.scheduled_time = 0  # Force immediate capture

        # Draw something to the screen
        self.screen.fill(BACKGROUND)
        pygame.display.flip()

        # Update should capture the screenshot
        self.screenshot.update(self.screen)

        # Check if a screenshot was saved
        screenshots = os.listdir(self.screenshot.directory)
        self.assertEqual(len(screenshots), 1)
        self.assertTrue(screenshots[0].startswith("snake_"))
        self.assertTrue(screenshots[0].endswith(".png"))


class TestGameRenderer(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.renderer = GameRenderer()

    def tearDown(self):
        """Clean up after each test."""
        pygame.quit()

    def test_start_menu_rendering(self):
        """Test start menu rendering."""
        GameRenderer.show_start_menu(self.screen)

        # Get the screen's pixel array
        pixel_array = pygame.surfarray.array3d(self.screen)

        # Check if the screen is not empty (has some non-background pixels)
        self.assertTrue((pixel_array != BACKGROUND).any())

    def test_game_over_rendering(self):
        """Test game over screen rendering."""
        score = 100
        high_score = 200
        GameRenderer.show_game_over(self.screen, score, high_score)

        # Get the screen's pixel array
        pixel_array = pygame.surfarray.array3d(self.screen)

        # Check if the screen is not empty (has some non-background pixels)
        self.assertTrue((pixel_array != BACKGROUND).any())

    def test_score_display(self):
        """Test score display in game."""
        score = 100
        high_score = 200

        # Create mock game objects
        class MockObject:
            def render(self, screen):
                pass

        snake = MockObject()
        food = MockObject()
        obstacles = MockObject()

        GameRenderer.render_game(self.screen, snake, food, obstacles, game_over=False, score=score, high_score=high_score)

        # Get the screen's pixel array
        pixel_array = pygame.surfarray.array3d(self.screen)

        # Check if the screen is not empty (has some non-background pixels)
        self.assertTrue((pixel_array != BACKGROUND).any())

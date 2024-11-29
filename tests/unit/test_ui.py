import os
import unittest
import pygame

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
        self.renderer.show_start_menu(self.screen)

        # Get the screen's pixel array
        pixel_array = pygame.surfarray.array3d(self.screen)

        # Check if the screen is not empty (has some non-background pixels)
        self.assertTrue((pixel_array != BACKGROUND).any())

    def test_game_over_rendering(self):
        """Test game over screen rendering."""
        score = 100
        high_score = 200
        self.renderer.show_game_over(self.screen, score, high_score)

        # Get the screen's pixel array
        pixel_array = pygame.surfarray.array3d(self.screen)

        # Check if the screen is not empty (has some non-background pixels)
        self.assertTrue((pixel_array != BACKGROUND).any())

    def test_score_display(self):
        """Test score display in game."""
        score = 100
        high_score = 200
        start_time = pygame.time.get_ticks()

        # Create mock game objects
        class MockObject:
            def render(self, screen):
                pass

        snake = MockObject()
        food = MockObject()
        obstacles = MockObject()

        self.renderer.render_game(self.screen, snake, food, obstacles, score, high_score, start_time)

        # Get the screen's pixel array
        pixel_array = pygame.surfarray.array3d(self.screen)

        # Check if the screen is not empty (has some non-background pixels)
        self.assertTrue((pixel_array != BACKGROUND).any())

    def test_pause_menu_rendering(self):
        """Test pause menu rendering."""
        score = 100
        self.renderer.show_pause_menu(self.screen, score)

        # Get the screen's pixel array to verify rendering
        pixel_array = pygame.surfarray.array3d(self.screen)
        self.assertTrue((pixel_array != BACKGROUND).any())

    def test_game_rendering_with_screenshot(self):
        """Test game rendering with screenshot manager."""

        class MockObject:
            def render(self, screen):
                pass

            def get_head(self):
                return (100, 100)

            def get_body(self):
                return [(90, 100), (80, 100)]

        snake = MockObject()
        food = MockObject()
        obstacles = MockObject()
        screenshot_manager = Screenshot()
        start_time = pygame.time.get_ticks()

        # Test rendering with screenshot manager
        self.renderer.render_game(self.screen, snake, food, obstacles, score=100, high_score=200, start_time=start_time, screenshot_manager=screenshot_manager)

        # Verify screen has been modified
        pixel_array = pygame.surfarray.array3d(self.screen)
        self.assertTrue((pixel_array != BACKGROUND).any())

        # Clean up screenshot directory
        if os.path.exists(screenshot_manager.directory):
            for file in os.listdir(screenshot_manager.directory):
                os.remove(os.path.join(screenshot_manager.directory, file))
            os.rmdir(screenshot_manager.directory)

    def test_cached_background(self):
        """Test that background is properly cached."""
        # Get initial background state
        initial_background = pygame.surfarray.array3d(self.renderer.background)

        # Create new renderer
        new_renderer = GameRenderer()
        new_background = pygame.surfarray.array3d(new_renderer.background)

        # Verify backgrounds are identical
        self.assertTrue((initial_background == new_background).all())

    def test_font_rendering(self):
        """Test font rendering in different game states."""
        # Test start menu text
        self.renderer.show_start_menu(self.screen)
        start_screen = pygame.surfarray.array3d(self.screen)
        self.assertTrue((start_screen != BACKGROUND).any())

        # Test game over text
        self.renderer.show_game_over(self.screen, score=100, high_score=200)
        game_over_screen = pygame.surfarray.array3d(self.screen)
        self.assertTrue((game_over_screen != BACKGROUND).any())
        self.assertFalse((game_over_screen == start_screen).all())

        # Test pause menu text
        self.renderer.show_pause_menu(self.screen, score=100)
        pause_screen = pygame.surfarray.array3d(self.screen)
        self.assertTrue((pause_screen != BACKGROUND).any())
        self.assertFalse((pause_screen == game_over_screen).all())

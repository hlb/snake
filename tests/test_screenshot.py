import os
import shutil
import pygame
from unittest import TestCase, main
from snake_game import Screenshot


class TestScreenshot(TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.Surface((800, 600))
        self.test_dir = "test_screenshots"
        os.makedirs(self.test_dir, exist_ok=True)
        self.screenshot = Screenshot()
        self.screenshot.directory = self.test_dir

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        pygame.quit()

    def test_init(self):
        """Test Screenshot initialization"""
        self.assertFalse(self.screenshot.pending)
        self.assertEqual(self.screenshot.scheduled_time, 0)
        self.assertEqual(self.screenshot.delay_ms, 500)
        self.assertTrue(os.path.exists(self.test_dir))

    def test_schedule(self):
        """Test screenshot scheduling"""
        current_time = pygame.time.get_ticks()
        self.screenshot.schedule()

        self.assertTrue(self.screenshot.pending)
        self.assertEqual(self.screenshot.scheduled_time, current_time + self.screenshot.delay_ms)

    def test_update_not_pending(self):
        """Test update when no screenshot is pending"""
        initial_files = os.listdir(self.test_dir) if os.path.exists(self.test_dir) else []
        self.screenshot.update(self.screen)
        final_files = os.listdir(self.test_dir)
        self.assertEqual(initial_files, final_files)

    def test_update_pending_but_not_time(self):
        """Test update when screenshot is pending but time hasn't elapsed"""
        self.screenshot.schedule()
        initial_files = os.listdir(self.test_dir)
        self.screenshot.update(self.screen)
        final_files = os.listdir(self.test_dir)
        self.assertEqual(initial_files, final_files)
        self.assertTrue(self.screenshot.pending)

    def test_update_pending_and_time_elapsed(self):
        """Test update when screenshot should be taken"""
        self.screenshot.schedule()
        self.screenshot.scheduled_time = 0  # Force time to have elapsed
        initial_files = os.listdir(self.test_dir)
        self.screenshot.update(self.screen)
        final_files = os.listdir(self.test_dir)

        # Should have one new file
        self.assertEqual(len(final_files), len(initial_files) + 1)
        self.assertFalse(self.screenshot.pending)


if __name__ == "__main__":
    main()

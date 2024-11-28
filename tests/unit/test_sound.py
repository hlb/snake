import unittest
import os
import pygame
from src.sound import SoundManager


class TestSoundManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize pygame for all tests."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Clean up pygame after all tests."""
        pygame.quit()

    def setUp(self):
        """Set up test environment before each test."""
        self.sound_manager = SoundManager()

    def test_sound_initialization(self):
        """Test sound system initialization."""
        self.assertIsNotNone(self.sound_manager)
        self.assertEqual(pygame.mixer.get_num_channels(), 8)

    def test_load_nonexistent_sound(self):
        """Test loading a non-existent sound file."""
        sound = self.sound_manager.load_sound("nonexistent.wav")
        self.assertIsNone(sound)

    def test_sound_volume_control(self):
        """Test volume control for sound effects."""
        # Skip sound generation test and just test the eat sound
        if self.sound_manager.eat_sound:
            original_volume = self.sound_manager.eat_sound.get_volume()

            self.sound_manager.eat_sound.set_volume(0.5)
            self.assertAlmostEqual(self.sound_manager.eat_sound.get_volume(), 0.5, places=1)

            self.sound_manager.eat_sound.set_volume(0.0)
            self.assertAlmostEqual(self.sound_manager.eat_sound.get_volume(), 0.0, places=1)

            self.sound_manager.eat_sound.set_volume(1.0)
            self.assertAlmostEqual(self.sound_manager.eat_sound.get_volume(), 1.0, places=1)

            # Restore original volume
            self.sound_manager.eat_sound.set_volume(original_volume)

    def test_background_music_control(self):
        """Test background music control."""
        # Test starting background music
        self.sound_manager.play_background_music()
        channel = pygame.mixer.Channel(0)
        self.assertTrue(channel.get_busy())

        # Test background music volume
        self.assertAlmostEqual(channel.get_volume(), 0.8, places=1)

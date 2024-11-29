import os
import unittest
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
        sound_manager = SoundManager()
        self.assertIsNotNone(sound_manager.background_channel)
        self.assertEqual(pygame.mixer.get_num_channels(), 8)

    def test_load_nonexistent_sound(self):
        """Test loading a non-existent sound file."""
        result = self.sound_manager.load_sound("nonexistent.wav")
        self.assertIsNone(result)

    def test_sound_volume_control(self):
        """Test volume control for sound effects."""
        sound_manager = SoundManager()

        # Test background music volume
        self.assertAlmostEqual(sound_manager.background_channel.get_volume(), 0.8, places=2)

        # Test eat sound volume
        if sound_manager.eat_sound:
            self.assertAlmostEqual(sound_manager.eat_sound.get_volume(), 0.4, places=2)

    def test_background_music_control(self):
        """Test background music control."""
        # Test starting background music
        self.sound_manager.play_background_music()
        channel = pygame.mixer.Channel(0)
        self.assertTrue(channel.get_busy())

        # Test background music volume
        self.assertAlmostEqual(channel.get_volume(), 0.8, places=1)

    def test_background_music_controls(self):
        """Test background music control functions."""
        sound_manager = SoundManager()

        # Test play
        sound_manager.play_background_music()
        self.assertTrue(sound_manager.background_channel.get_busy())

        # Test pause
        sound_manager.pause_background_music()

        # Test resume
        sound_manager.resume_background_music()
        self.assertTrue(sound_manager.background_channel.get_busy())

    def test_sound_effects(self):
        """Test sound effects playback."""
        sound_manager = SoundManager()

        # Test eat sound
        sound_manager.play_eat_sound()
        # Verify eat sound is loaded
        self.assertIsNotNone(sound_manager.eat_sound)

        # Test crash sound
        sound_manager.play_crash_sound()
        # Verify crash sound is loaded
        self.assertIsNotNone(sound_manager.crash_sound)

    def test_missing_sound_file(self):
        """Test handling of missing sound files."""
        sound_manager = SoundManager()

        # Try to load non-existent sound
        result = sound_manager.load_sound("nonexistent.wav")
        self.assertIsNone(result)

    def test_invalid_sound_file(self):
        """Test handling of invalid sound files."""
        # Create an empty file that's not a valid sound file
        with open("invalid.wav", "w", encoding="utf-8") as f:
            f.write("not a sound file")

        sound_manager = SoundManager()
        result = sound_manager.load_sound("invalid.wav")
        self.assertIsNone(result)

        # Clean up
        os.remove("invalid.wav")

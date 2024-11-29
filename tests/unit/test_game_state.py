import unittest
import os
from src.game_state import GameState


class TestGameState(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.game_state = GameState()
        # Remove test high score file if it exists
        if os.path.exists("high_score.txt"):
            os.remove("high_score.txt")

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists("high_score.txt"):
            os.remove("high_score.txt")

    def test_initial_state(self):
        """Test initial game state values."""
        self.assertEqual(self.game_state.score, 0)
        self.assertEqual(self.game_state.high_score, 0)
        self.assertFalse(self.game_state.is_game_over)
        self.assertFalse(self.game_state.is_playing)

    def test_start_game(self):
        """Test game start state transition."""
        self.game_state.score = 10  # Set some previous score
        self.game_state.is_game_over = True

        self.game_state.start_game()

        self.assertEqual(self.game_state.score, 0)
        self.assertFalse(self.game_state.is_game_over)
        self.assertTrue(self.game_state.is_playing)

    def test_end_game(self):
        """Test game end state transition."""
        self.game_state.score = 10
        self.game_state.is_playing = True

        self.game_state.end_game()

        self.assertTrue(self.game_state.is_game_over)
        self.assertFalse(self.game_state.is_playing)

    def test_high_score_persistence(self):
        """Test high score saving and loading."""
        # Set and save a high score
        self.game_state.score = 100
        self.game_state.end_game()  # This should save the high score

        # Create a new game state instance
        new_game_state = GameState()
        self.assertEqual(new_game_state.high_score, 100)

    def test_update_score(self):
        """Test score updates and high score tracking."""
        self.game_state.update_score(50)
        self.assertEqual(self.game_state.score, 50)
        self.assertEqual(self.game_state.high_score, 50)

        # Score below high score shouldn't update high score
        self.game_state.update_score(30)
        self.assertEqual(self.game_state.score, 30)
        self.assertEqual(self.game_state.high_score, 50)

        # Score above high score should update high score
        self.game_state.update_score(60)
        self.assertEqual(self.game_state.score, 60)
        self.assertEqual(self.game_state.high_score, 60)

    def test_toggle_pause(self):
        """Test game pause toggling."""
        self.assertFalse(self.game_state.is_playing)

        self.game_state.toggle_pause()
        self.assertTrue(self.game_state.is_playing)

        self.game_state.toggle_pause()
        self.assertFalse(self.game_state.is_playing)
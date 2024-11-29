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
        # Game should start in non-playing state
        self.assertFalse(self.game_state.is_playing)
        self.assertFalse(self.game_state.is_paused)

        # Start the game
        self.game_state.start_game()
        self.assertTrue(self.game_state.is_playing)
        self.assertFalse(self.game_state.is_paused)

        # Pause the game
        self.game_state.toggle_pause()
        self.assertTrue(self.game_state.is_playing)  # Game should still be "playing"
        self.assertTrue(self.game_state.is_paused)  # But in paused state

        # Unpause the game
        self.game_state.toggle_pause()
        self.assertTrue(self.game_state.is_playing)
        self.assertFalse(self.game_state.is_paused)

    def test_high_score_file_not_found(self):
        """Test loading high score when file doesn't exist."""
        # Ensure file doesn't exist
        if os.path.exists("high_score.txt"):
            os.remove("high_score.txt")

        game_state = GameState()
        self.assertEqual(game_state.high_score, 0)

    def test_high_score_invalid_content(self):
        """Test loading high score with invalid file content."""
        # Create file with invalid content
        with open("high_score.txt", "w", encoding="utf-8") as f:
            f.write("invalid")

        game_state = GameState()
        self.assertEqual(game_state.high_score, 0)

        # Clean up
        os.remove("high_score.txt")

    def test_high_score_save_load(self):
        """Test saving and loading high score."""
        game_state = GameState()
        game_state.high_score = 100
        game_state.save_high_score()

        # Create new instance to load the saved score
        new_game_state = GameState()
        self.assertEqual(new_game_state.high_score, 100)

        # Clean up
        os.remove("high_score.txt")

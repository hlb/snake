class GameState:
    def __init__(self):
        self.score = 0
        self.high_score = self.load_high_score()
        self.start_time = 0
        self.is_game_over = False
        self.is_playing = False
        self.is_paused = False

    def load_high_score(self):
        """Load the high score from file."""
        try:
            with open("high_score.txt", "r", encoding="utf-8") as f:
                return int(f.read())
        except FileNotFoundError:
            return 0
        except ValueError:
            return 0

    def save_high_score(self):
        """Save the current high score to file."""
        with open("high_score.txt", "w", encoding="utf-8") as f:
            f.write(str(self.high_score))

    def update_score(self, new_score):
        """Update the current score and high score if necessary."""
        self.score = new_score
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def start_game(self):
        """Start a new game."""
        self.score = 0
        self.is_game_over = False
        self.is_playing = True
        self.is_paused = False

    def end_game(self):
        """End the current game."""
        self.is_game_over = True
        self.is_playing = False
        self.is_paused = False
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def toggle_pause(self):
        """Toggle the game's pause state."""
        if self.is_playing and not self.is_game_over:
            self.is_paused = not self.is_paused

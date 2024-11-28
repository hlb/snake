# Modern Python Snake Game

A modern take on the classic Snake game, built with Python and Pygame. Experience smooth animations, dynamic visuals, and engaging gameplay mechanics.

![Snake Game Screenshot](docs/screenshot.png)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/snake-game.git
cd snake-game

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch the game
python snake_game.py
```

## Gameplay

### Controls
| Key | Action |
|-----|--------|
| ENTER | Start game / Restart after game over |
| ↑ | Move up |
| ↓ | Move down |
| ← | Move left |
| → | Move right |
| Q | Quit game |

### Power-ups and Scoring
The game features three types of collectible food items:

- 🍎 **Normal Food**
  - Basic food item
  - Adds 1 point to score
  - Increases snake length

- ⭐ **Golden Food**
  - Rare, valuable food
  - Adds 2 points to score
  - Increases snake length

- 🚀 **Speed Food**
  - Special power-up
  - Temporarily boosts snake speed
  - Adds 1 point to score

### Game Mechanics
- Snake wraps around screen edges for continuous gameplay
- Colliding with obstacles or snake's body ends the game
- Score increases with each food item collected
- Background music and sound effects enhance the experience

## Acknowledgments

### Music
- Background Music: ["The Snake Game (original GB music)"](https://youtu.be/FpDWpX9luCQ?si=zP7c-KROsUjh8SQ5) by Zuka

## Development

### Prerequisites
- Python 3.11 or higher
- Pygame library
- Virtual environment (recommended)

### Project Structure
```
snake/
├── src/               # Source code
├── tests/             # Test suite
├── sounds/            # Audio files
├── requirements.txt   # Dependencies
└── README.md         # Documentation
```

### Running Tests
The project includes comprehensive unit and integration tests:

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test suite
python -m unittest tests/unit/test_snake.py -v
```

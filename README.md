# Snake Game

## About

This is a Snake game implementation that demonstrates how [Windsurf](https://codeium.com/windsurf) can be used to develop and maintain software. The entire codebase, including game logic, tests, and documentation, has been written with the assistance of Windsurf.

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

# Launch with automatic screenshots (captures when eating food)
python snake_game.py --screenshots
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
| ESC | Pause/Resume game |
| Q | Quit game |

### Power-ups and Scoring
The game features five types of collectible food items:

- 🍕 **Normal Food**
  - Basic food items (🍕🍇🍪🍓)
  - Adds 1 point to score
  - Increases snake length

- 🌟 **Golden Food**
  - Rare, valuable food items (🌟⭐🌞)
  - Adds 2 points to score
  - Increases snake length

- ⚡ **Speed Food**
  - Speed boost power-up (⚡🚀💨)
  - Temporarily increases snake speed
  - Adds 1 point to score
  - Effect duration is temporary

- 🐌 **Slow Food**
  - Speed reduction power-up (🐌🦥🐢)
  - Temporarily decreases snake speed
  - Adds 1 point to score
  - Effect duration is temporary

- 👻 **Ghost Food**
  - Rare ghost power-up (👻)
  - Temporarily allows passing through obstacles
  - Adds 1 point to score
  - Makes snake translucent during effect
  - 8-second duration with visual countdown

### Game Mechanics
- Snake wraps around screen edges for continuous gameplay
- Colliding with obstacles or snake's body ends the game
- Score increases based on food type collected
- Speed effects are temporary and stack with base speed
- Base speed increases every 10 points
- High score system tracks best performance
- Game timer shows elapsed time
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
├── tests/            # Test suite
│   ├── unit/        # Unit tests
│   └── integration/ # Integration tests
├── sounds/           # Audio files
├── requirements.txt  # Dependencies
└── README.md        # Documentation
```

### Running Tests
The project includes comprehensive unit and integration tests:

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test categories
python -m unittest tests/unit/test_snake.py -v     # Snake mechanics
python -m unittest tests/integration/*.py -v       # Integration tests
```

### Code Coverage

To run code coverage:

```bash
python -m pytest --cov=.
coverage html  # generates HTML report in htmlcov/
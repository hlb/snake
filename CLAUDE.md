# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a Snake game implementation in Python using Pygame. The game features modern graphics, special effects, sound, and enhanced gameplay mechanics including different food types, obstacles, and power-ups.

## Development Commands

### Environment Setup
```bash
# Set up Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Game
```bash
# Launch the game
python snake_game.py

# Launch with automatic screenshots
python snake_game.py --screenshots
```

### Testing
```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test categories
python -m unittest tests/unit/test_snake.py -v
python -m unittest tests/integration/*.py -v

# Run with coverage
python -m pytest --cov=.
coverage html  # generates HTML report in htmlcov/
```

### Code Quality
```bash
# Run linting
pylint src/ tests/

# Format code
black src/ tests/ snake_game.py

# Run pre-commit hooks
pre-commit run --all-files
```

## Architecture

### Core Components Structure
- `src/` - Main source code directory with modular components
- `snake_game.py` - Main game loop and entry point
- `src/game_state.py` - Handles game state transitions (menu, playing, paused, game over)
- `src/snake.py` - Snake mechanics, movement, and collision detection
- `src/food.py` - Food system with 4 types (normal, golden, speed, slow)
- `src/obstacle.py` - Dynamic obstacle generation (every 10 points)
- `src/sound.py` - Audio management with error handling
- `src/ui.py` - Rendering system (GameRenderer and Screenshot classes)
- `src/constants.py` - Game configuration and constants

### Key Game Logic
- Grid-based movement system (40px grid size, 20x15 grid)
- Snake wraps around screen edges
- Speed increases every 10 points (range: 2-12)
- Food types with different effects and point values
- Effect stacking system for speed modifications
- High score persistence in `high_score.txt`

### Food System Details
- Normal Food (50%): Basic items, +1 point
- Golden Food (15%): Valuable items, +2 points  
- Speed Food (15%): Temporary speed boost, +1 point
- Slow Food (15%): Temporary speed reduction, +1 point
- Ghost Food (5%): Rare power-up, allows passing through obstacles, +1 point, 8-second duration

### Testing Architecture
- `tests/test_base.py` - Base test class with Pygame setup/teardown
- `tests/unit/` - Component-specific unit tests
- `tests/integration/` - Game mechanics and UI integration tests
- Coverage reports generated in `htmlcov/`

## Important Notes
- All components use modular design with clear separation of concerns
- Sound files are optional - game handles missing audio gracefully  
- Screenshot system can capture automatic screenshots when eating food
- Game state persists high scores across sessions
- Pre-commit hooks ensure code quality before commits
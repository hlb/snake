# Python Snake Game

A modern-style Snake game created with Python and Pygame.

## Features

- Modern visual design with smooth animations
- Rounded snake body and food with emoji graphics
- Dynamic background grid
- Game over screen with final score
- Real-time score display
- Sound effects for eating and game over
- Boundary wrapping (snake can pass through walls)
- Smooth controls with immediate response

## Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

1. Make sure the virtual environment is activated
2. Run the game:
```bash
python snake_game.py
```

## Game Controls

- Press ENTER to start the game
- ↑ Move up
- ↓ Move down
- ← Move left
- → Move right
- Space - Restart when game is over
- Q - Quit game

## Game Rules

1. Use arrow keys to control snake movement
2. Eating food increases score and snake length
3. Hitting yourself ends the game
4. Can pass through boundaries to reach the opposite side

## Running Tests

```bash
python -m unittest test_snake_game.py -v

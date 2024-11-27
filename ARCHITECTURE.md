# Snake Game Architecture Document

## Project Overview
Modern Snake Game is a Python-based implementation of the classic Snake game, featuring modern graphics, special effects, and enhanced gameplay mechanics.

## Directory Structure
```
snake/
├── src/                    # Source code directory
│   ├── __init__.py        # Package initialization
│   ├── constants.py       # Game constants and configurations
│   ├── snake.py          # Snake class implementation
│   ├── food.py           # Food class implementation
│   └── obstacle.py       # Obstacle class implementation
├── tests/                 # Test suite directory
│   ├── base_test.py      # Base test class with common utilities
│   ├── unit/             # Unit tests directory
│   │   ├── test_snake.py     # Snake component tests
│   │   ├── test_food.py      # Food system tests
│   │   └── test_obstacle.py  # Obstacle system tests
│   └── integration/      # Integration tests directory
│       ├── test_game_mechanics.py  # Game mechanics tests
│       └── test_ui.py           # UI rendering tests
├── sounds/                # Sound effects directory
│   ├── eat.wav           # Food consumption sound
│   ├── crash.wav         # Collision sound
│   └── background.wav    # Background music
├── docs/                 # Documentation assets
│   └── screenshot.png    # Game screenshot
├── snake_game.py         # Main game entry point
└── README.md             # Project documentation

```

## Core Components

### 1. Game Engine (snake_game.py)
- **Responsibility**: Main game loop and state management
- **Key Features**:
  - Game state handling (menu, playing, game over)
  - Event processing
  - Rendering coordination
  - Sound system management
  - Score tracking

### 2. Snake (src/snake.py)
- **Responsibility**: Snake behavior and properties
- **Key Features**:
  - Movement mechanics
  - Growth system
  - Collision detection
  - Special effects handling
- **State Management**:
  - Position tracking
  - Length
  - Base and current speed
  - Score
  - Effect timers

### 3. Food System (src/food.py)
- **Responsibility**: Food item management
- **Types**:
  - Normal Food (70% chance)
    - +1 point
    - Regular speed
  - Golden Apple (15% chance)
    - +2 points
    - Regular speed
  - Speed Fruit (15% chance)
    - +1 point
    - Temporary speed boost
- **Features**:
  - Random position generation
  - Collision avoidance with obstacles
  - Type-specific effects
  - Visual representation with emojis

### 4. Obstacle System (src/obstacle.py)
- **Responsibility**: Obstacle management
- **Features**:
  - Static obstacle placement
  - Collision detection
  - Position validation
  - Grid-based positioning

### 5. Constants (src/constants.py)
- **Responsibility**: Game configuration and constants
- **Categories**:
  - Window dimensions
  - Grid settings
  - Colors and visuals
  - Game speeds
  - Food properties
  - Direction vectors
  - Sound settings

## Testing Architecture

### Base Test Class (tests/base_test.py)
- **Responsibility**: Common test functionality
- **Features**:
  - Pygame initialization/cleanup
  - Test environment setup
  - Common assertions
  - Utility methods

### Unit Tests
- **Snake Tests** (test_snake.py):
  - Movement mechanics
  - Collision detection
  - Growth behavior
  - Speed modifications
  
- **Food Tests** (test_food.py):
  - Food generation
  - Effect application
  - Position randomization
  - Type distribution
  
- **Obstacle Tests** (test_obstacle.py):
  - Placement validation
  - Collision detection
  - Position management

### Integration Tests
- **Game Mechanics** (test_game_mechanics.py):
  - State transitions
  - Score management
  - Reset functionality
  - Direction changes
  
- **UI Tests** (test_ui.py):
  - Menu rendering
  - Game screen rendering
  - Score display
  - Game over screen

## Game States and Transitions

```mermaid
stateDiagram-v2
    [*] --> Menu
    Menu --> Playing: ENTER pressed
    Playing --> GameOver: Collision
    GameOver --> Playing: ENTER pressed
    Playing --> [*]: Q pressed
    GameOver --> [*]: Q pressed
```
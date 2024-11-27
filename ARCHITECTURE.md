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
├── sounds/                # Sound effects directory
│   ├── eat.wav           # Food consumption sound
│   ├── crash.wav         # Collision sound
│   └── background.wav    # Background music
├── snake_game.py         # Main game entry point
├── test_snake_game.py    # Unit tests
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

### 2. Snake (src/snake.py)
- **Responsibility**: Snake behavior and properties
- **Key Features**:
  - Movement mechanics
  - Growth system
  - Collision detection
  - Special effects handling (speed modifications)
- **State Management**:
  - Position tracking
  - Length
  - Speed
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
  - Dynamic obstacle placement
  - Collision detection
  - Progressive difficulty (new obstacles added every 10 points)

### 5. Constants (src/constants.py)
- **Responsibility**: Game configuration and constants
- **Categories**:
  - Window dimensions
  - Grid settings
  - Colors
  - Game speeds
  - Food properties
  - Direction vectors

## Game Mechanics

### Movement System
- Grid-based movement
- Four directions (UP, DOWN, LEFT, RIGHT)
- Boundary wrapping (snake passes through walls)
- Smooth controls with immediate response

### Scoring System
- Normal food: +1 point
- Golden apple: +2 points
- Score display in real-time
- High score tracking

### Special Effects System
- **Speed Boost**:
  - Duration: 5 seconds
  - Speed increase: +2 units
  - Automatic reversion to normal speed
- **Visual Feedback**:
  - Unique colors for different food types
  - Emoji-based food representation
- **Sound Effects**:
  - Eating sound
  - Collision sound
  - Background music

## System Architecture Diagrams

### Class Diagram
```mermaid
classDiagram
    class Snake {
        +List positions
        +Tuple direction
        +int score
        +int speed
        +int length
        +int effect_end_time
        +update(obstacles)
        +handle_food_effect(food)
        +render(screen)
    }
    
    class Food {
        +Tuple position
        +str type
        +Dict properties
        +str emoji
        +Surface emoji_surface
        +randomize_position()
        +render(screen)
    }
    
    class Obstacle {
        +Set positions
        +add_obstacle(snake)
        +render(screen)
    }
    
    class GameEngine {
        +Surface screen
        +bool game_over
        +bool game_started
        +handle_events()
        +update()
        +render()
        +run()
    }
    
    GameEngine --> Snake : manages
    GameEngine --> Food : manages
    GameEngine --> Obstacle : manages
    Snake ..> Obstacle : checks collision
    Food ..> Obstacle : avoids collision
```

### Component Interaction
```mermaid
sequenceDiagram
    participant GameLoop
    participant Snake
    participant Food
    participant Obstacle
    
    GameLoop->>Snake: Update position
    Snake->>Obstacle: Check collision
    Obstacle-->>Snake: Collision result
    
    alt Collision detected
        Snake-->>GameLoop: Game over
    else No collision
        GameLoop->>Food: Check if eaten
        alt Food eaten
            Food->>Snake: Apply effect
            Food->>Food: Randomize position
            alt Score multiple of 10
                GameLoop->>Obstacle: Add new obstacle
            end
        end
    end
    
    GameLoop->>GameLoop: Render frame
```

### State Diagram
```mermaid
stateDiagram-v2
    [*] --> Menu
    Menu --> Playing: ENTER pressed
    Playing --> GameOver: Collision
    GameOver --> Playing: SPACE pressed
    GameOver --> [*]: Q pressed
    Playing --> Playing: Movement keys
    
    state Playing {
        [*] --> Normal
        Normal --> SpeedBoost: Speed fruit eaten
        SpeedBoost --> Normal: Duration expired
        Normal --> Normal: Normal food eaten
        Normal --> Normal: Golden apple eaten
    }
```

### Food Type Distribution
```mermaid
pie
    title "Food Type Probability Distribution"
    "Normal Food" : 70
    "Golden Apple" : 15
    "Speed Fruit" : 15
```

## Testing Architecture

### Unit Tests (test_snake_game.py)
- **Core Functionality Tests**:
  - Snake movement
  - Collision detection
  - Food generation
  - Obstacle placement
- **Special Feature Tests**:
  - Food type properties
  - Special effects
  - Score calculation
  - Speed modifications

## Future Enhancements
1. **Planned Features**:
   - Leaderboard system
   - Additional power-ups
   - Multiple difficulty levels
   - Custom themes

2. **Technical Improvements**:
   - Save/load game state
   - Configuration file support
   - Performance optimizations
   - Mobile device support

## Design Patterns
- **Singleton**: Game state management
- **Observer**: Event handling system
- **Factory**: Food type generation
- **State**: Game state transitions

## Dependencies
- Python 3.x
- Pygame: Graphics and sound
- Pygame-emojis: Food visualization

## Development Guidelines
1. **Code Style**:
   - Follow PEP 8
   - Use type hints
   - Document all classes and methods

2. **Testing**:
   - Write tests for new features
   - Maintain test coverage
   - Test edge cases

3. **Version Control**:
   - Feature branches
   - Descriptive commit messages
   - Regular testing before commits

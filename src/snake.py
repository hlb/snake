import random
from dataclasses import dataclass
import pygame
from .constants import (
    GRID_WIDTH,
    GRID_HEIGHT,
    GRID_SIZE,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    draw_rounded_rect,
)
from .particle_system import ParticleSystem


@dataclass
class SnakeEffects:
    """Properties related to snake effects and visuals."""

    base_speed: int = 6  # Keep track of base speed
    effect_end_time: int = 0  # Track when speed effect ends
    gradient_colors: list[tuple[int, int, int]] = None  # Snake gradient colors

    def __post_init__(self):
        if self.gradient_colors is None:
            self.gradient_colors = [
                (50, 205, 50),  # Light green
                (34, 139, 34),  # Forest green
                (0, 100, 0),  # Dark green
            ]


class Snake:
    def __init__(self):
        """Initialize a new snake with default settings."""
        # Essential attributes kept for testing
        self.score = 0
        self.speed = 6  # Initial speed
        self.length = 3
        self.positions = []  # Will be set in _initialize_snake
        self.direction = None  # Will be set in _initialize_snake

        # Group other attributes in a dataclass
        self.effects = SnakeEffects()
        self.particle_system = ParticleSystem()
        self._initialize_snake()

    def _initialize_snake(self):
        """Initialize or reset snake's position and length."""
        self.length = 3
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        # Start at center
        center = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.positions = [center]
        # Add body segments behind head based on direction
        dx, dy = self.direction
        for i in range(1, self.length):
            self.positions.append(((center[0] - dx * i) % GRID_WIDTH, (center[1] - dy * i) % GRID_HEIGHT))

    def get_head_position(self):
        """Return the position of snake's head."""
        return self.positions[0]

    def _check_collision(self, new_pos, obstacles):
        """Check if the new position results in a collision."""
        # Check collision with obstacles
        if new_pos in obstacles.positions:
            return True
        # Check collision with self (excluding the tail which will move)
        if new_pos in self.positions[:-1]:
            return True
        return False

    def handle_food_effect(self, food_properties):
        """Handle the effects of different food types."""
        # Handle speed change only
        if food_properties["speed_change"] != 0:
            self.effects.base_speed = self.speed  # Store current base speed
            self.speed += food_properties["speed_change"]  # Apply speed change directly
            self.speed = max(2, min(self.speed, 12))  # Keep speed between 2 and 12
            if food_properties["duration"] > 0:
                self.effects.effect_end_time = pygame.time.get_ticks() + food_properties["duration"]

    def update(self, obstacles):
        """Update snake position and check for collisions."""
        # Check if speed effect should end
        current_time = pygame.time.get_ticks()
        if self.effects.effect_end_time > 0 and current_time >= self.effects.effect_end_time:
            self.speed = self.effects.base_speed
            self.effects.effect_end_time = 0

        current = self.get_head_position()
        dx, dy = self.direction
        new_head = ((current[0] + dx) % GRID_WIDTH, (current[1] + dy) % GRID_HEIGHT)

        # Check for collisions
        if self._check_collision(new_head, obstacles):
            return True  # Collision detected

        # Move snake
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

        return False  # No collision

    def render(self, screen):
        """Render the snake on the screen."""
        # Update and render particles
        self.particle_system.update()
        self.particle_system.render(screen)

        # Render snake with gradient
        for i, pos in enumerate(self.positions):
            # Calculate gradient color based on position in snake
            gradient_index = (i * len(self.effects.gradient_colors)) // len(self.positions)
            color = self.effects.gradient_colors[min(gradient_index, len(self.effects.gradient_colors) - 1)]

            rect = pygame.Rect(
                pos[0] * GRID_SIZE + 2,
                pos[1] * GRID_SIZE + 2,
                GRID_SIZE - 4,
                GRID_SIZE - 4,
            )
            draw_rounded_rect(screen, color, rect, 10)

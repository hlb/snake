import random
import pygame
from .constants import (
    GRID_WIDTH,
    GRID_HEIGHT,
    OBSTACLE_COLOR,
    GRID_SIZE,
    OBSTACLE_COUNT,
    draw_rounded_rect,
)


class Obstacle:
    def __init__(self):
        self.positions = set()
        self.color = OBSTACLE_COLOR
        self.generate_obstacles(OBSTACLE_COUNT)  # Initial number of obstacles

    def generate_obstacles(self, count):
        """Generate specified number of obstacles"""
        self.positions.clear()
        while len(self.positions) < count:
            pos = (
                random.randint(2, GRID_WIDTH - 3),
                random.randint(2, GRID_HEIGHT - 3),
            )
            # Ensure obstacles are not generated near the snake's initial position
            if (
                pos[0] < GRID_WIDTH // 2 - 2
                or pos[0] > GRID_WIDTH // 2 + 2
                or pos[1] < GRID_HEIGHT // 2 - 2
                or pos[1] > GRID_HEIGHT // 2 + 2
            ):
                self.positions.add(pos)

    def add_obstacle(self, snake):
        """Add a new obstacle, avoiding placement directly in front of the snake"""
        head = snake.get_head_position()
        direction = snake.direction

        # Calculate the three grid cells in front of the snake's head
        danger_positions = set()
        x, y = head
        dx, dy = direction
        for i in range(3):  # Check the three cells in front
            x = (x + dx) % GRID_WIDTH
            y = (y + dy) % GRID_HEIGHT
            danger_positions.add((x, y))
            # Add the cells to the left and right
            danger_positions.add(
                ((x + dy) % GRID_WIDTH, (y - dx) % GRID_HEIGHT)
            )  # Left
            danger_positions.add(
                ((x - dy) % GRID_WIDTH, (y + dx) % GRID_HEIGHT)
            )  # Right

        # Try to place a new obstacle
        attempts = 100  # Maximum attempts
        while attempts > 0:
            pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )

            # Check if the position meets all conditions
            if (
                pos not in snake.positions
                and pos not in self.positions
                and pos not in danger_positions
            ):
                self.positions.add(pos)
                break
            attempts -= 1

    def render(self, screen):
        """Render all obstacles on the screen"""
        for pos in self.positions:
            rect = pygame.Rect(
                pos[0] * GRID_SIZE + 2,
                pos[1] * GRID_SIZE + 2,
                GRID_SIZE - 4,
                GRID_SIZE - 4,
            )
            draw_rounded_rect(screen, self.color, rect, 10)

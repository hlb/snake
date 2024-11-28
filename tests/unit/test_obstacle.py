from tests.test_base import SnakeGameTest
from src import GRID_WIDTH, GRID_HEIGHT, GRID_SIZE


class TestObstacle(SnakeGameTest):
    """Unit tests for Obstacle class functionality."""

    def test_obstacle_initialization(self):
        """Test obstacle initialization and placement."""
        self.assertTrue(len(self.obstacles.positions) > 0)
        for pos in self.obstacles.positions:
            self.assert_position_in_grid(pos)

    def test_obstacle_collision_detection(self):
        """Test obstacle collision detection."""
        # Clear existing obstacles and add one at a known position
        self.obstacles.positions.clear()
        test_obstacle_pos = (10, 10)
        self.obstacles.positions.add(test_obstacle_pos)

        # Test collision detection
        self.assertTrue(test_obstacle_pos in self.obstacles.positions)
        self.assertFalse((9, 9) in self.obstacles.positions)

    def test_obstacle_placement_validity(self):
        """Test that obstacles are placed in valid positions."""
        # Check that obstacles don't overlap with initial snake position
        snake_positions = set(self.snake.positions)
        self.assertTrue(snake_positions.isdisjoint(self.obstacles.positions))

        # Check that obstacles don't block all possible paths
        blocked_count = len(self.obstacles.positions)
        total_grid_size = GRID_WIDTH * GRID_HEIGHT
        self.assertTrue(blocked_count < total_grid_size / 4)  # Arbitrary threshold

    def test_dynamic_obstacle_generation(self):
        """Test dynamic obstacle generation."""
        # Clear existing obstacles
        initial_count = len(self.obstacles.positions)
        self.obstacles.positions.clear()

        # Add obstacle and verify it's placed correctly
        self.snake.positions = [(5, 5)]  # Set snake position
        self.snake.direction = (1, 0)  # Moving right

        # Add new obstacle
        self.obstacles.add_obstacle(self.snake)

        # Verify obstacle was added
        self.assertEqual(len(self.obstacles.positions), 1)

        # Verify obstacle is not in danger zone (3 cells in front of snake)
        danger_positions = {
            (6, 5),
            (7, 5),
            (8, 5),  # Direct front
            (6, 4),
            (7, 4),
            (8, 4),  # Above
            (6, 6),
            (7, 6),
            (8, 6),
        }  # Below

        obstacle_pos = next(iter(self.obstacles.positions))
        self.assertNotIn(obstacle_pos, danger_positions)
        self.assertNotIn(obstacle_pos, self.snake.positions)

    def test_obstacle_render(self):
        """Test obstacle rendering."""
        # Create a mock screen surface
        import pygame

        screen = pygame.Surface((800, 600))

        # Clear obstacles and add one at known position
        self.obstacles.positions.clear()
        test_pos = (5, 5)
        self.obstacles.positions.add(test_pos)

        # Render obstacles
        self.obstacles.render(screen)

        # Verify pixel color at obstacle position
        pixel_pos = (
            test_pos[0] * GRID_SIZE + GRID_SIZE // 2,
            test_pos[1] * GRID_SIZE + GRID_SIZE // 2,
        )
        color = screen.get_at(pixel_pos)
        self.assertEqual(color, self.obstacles.color)

    def test_obstacle_generation_edge_cases(self):
        """Test obstacle generation edge cases."""
        # Test generation with snake near grid edge
        self.obstacles.positions.clear()

        # Place snake at grid edge
        self.snake.positions = [(GRID_WIDTH - 1, GRID_HEIGHT - 1)]
        self.snake.direction = (1, 0)  # Moving right (will wrap around)

        # Add obstacle
        self.obstacles.add_obstacle(self.snake)

        # Verify obstacle placement
        self.assertEqual(len(self.obstacles.positions), 1)
        obstacle_pos = next(iter(self.obstacles.positions))

        # Check that obstacle is not in wrapped danger zone
        danger_positions = {
            (0, GRID_HEIGHT - 1),
            (1, GRID_HEIGHT - 1),
            (2, GRID_HEIGHT - 1),  # Front
            (0, GRID_HEIGHT - 2),
            (1, GRID_HEIGHT - 2),
            (2, GRID_HEIGHT - 2),  # Above
            (0, 0),
            (1, 0),
            (2, 0),
        }  # Below (wrapped)

        self.assertNotIn(obstacle_pos, danger_positions)
        self.assertNotIn(obstacle_pos, self.snake.positions)

    def test_multiple_obstacle_generation(self):
        """Test generating multiple obstacles."""
        # Clear existing obstacles
        self.obstacles.positions.clear()

        # Generate multiple obstacles
        test_count = 5
        self.obstacles.generate_obstacles(test_count)

        # Verify count and positions
        self.assertEqual(len(self.obstacles.positions), test_count)

        # Verify no obstacles in center area
        center_positions = set()
        for x in range(GRID_WIDTH // 2 - 2, GRID_WIDTH // 2 + 3):
            for y in range(GRID_HEIGHT // 2 - 2, GRID_HEIGHT // 2 + 3):
                center_positions.add((x, y))

        self.assertTrue(center_positions.isdisjoint(self.obstacles.positions))

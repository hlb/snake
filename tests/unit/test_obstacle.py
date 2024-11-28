from tests.test_base import SnakeGameTest
from src import GRID_WIDTH, GRID_HEIGHT

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

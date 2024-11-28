from tests.base_test import SnakeGameTest
from src import (
    GRID_WIDTH, GRID_HEIGHT, UP, DOWN, LEFT, RIGHT
)

class TestSnake(SnakeGameTest):
    """Unit tests for Snake class functionality."""

    def test_snake_initialization(self):
        """Test initial snake state and properties."""
        self.assertEqual(len(self.snake.positions), 3)
        self.assertEqual(self.snake.score, 0)
        self.assert_valid_direction(self.snake.direction)
        for pos in self.snake.positions:
            self.assert_position_in_grid(pos)

    def test_snake_movement(self):
        """Test basic snake movement in all directions."""
        # Test movement right
        self.snake = self.create_test_snake_at((10, 10), RIGHT)
        initial_head = self.snake.get_head_position()
        self.snake.update(self.obstacles)
        new_head = self.snake.get_head_position()
        self.assertEqual(new_head[0], (initial_head[0] + 1) % GRID_WIDTH)
        self.assertEqual(new_head[1], initial_head[1])

    def test_snake_collision_with_self(self):
        """Test snake collision with itself."""
        self.snake.positions = [(6, 5), (5, 5), (4, 5)]
        self.snake.direction = LEFT
        new_pos = ((6, 5)[0] + LEFT[0]) % GRID_WIDTH, ((6, 5)[1] + LEFT[1]) % GRID_HEIGHT
        self.assertTrue(self.snake._check_collision(new_pos, self.obstacles))

    def test_snake_collision_with_obstacle(self):
        """Test snake collision with obstacles."""
        self.snake = self.create_test_snake_at((5, 5))
        self.obstacles.positions = {(6, 5)}
        self.snake.direction = RIGHT
        new_pos = ((5, 5)[0] + RIGHT[0]) % GRID_WIDTH, ((5, 5)[1] + RIGHT[1]) % GRID_HEIGHT
        self.assertTrue(self.snake._check_collision(new_pos, self.obstacles))

    def test_snake_growth(self):
        """Test snake growth mechanics."""
        initial_length = len(self.snake.positions)
        self.snake.length += 1
        self.snake.update(self.obstacles)
        self.assertEqual(len(self.snake.positions), initial_length + 1)
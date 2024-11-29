import pygame
import pytest
from pygame.locals import K_UP, K_DOWN

from tests.test_base import SnakeGameTest
from src import Snake, Food, Obstacle, FOOD_TYPES, UP, RIGHT
from src.constants import NORMAL_FOOD_COLOR, GOLDEN_APPLE_COLOR, SPEED_FRUIT_COLOR, SLOW_FRUIT_COLOR
from src.game_state import GameState
from snake_game import handle_direction_change, update_game_state


# pylint: disable=protected-access,redefined-outer-name
class TestGameMechanics(SnakeGameTest):
    """Integration tests for game mechanics."""

    def setUp(self):
        """Set up test environment before each test."""
        super().setUp()

        # Create a mock sound manager
        class MockSoundManager:
            def play_eat_sound(self):
                pass

            def play_crash_sound(self):
                pass

        self.sound_manager = MockSoundManager()

    def test_game_reset(self):
        """Test game reset functionality."""
        # Modify game state
        self.game_state = GameState()
        self.game_state.score = 100
        self.snake.positions = [(1, 1)]

        # Reset game by creating new snake
        self.snake = Snake()
        self.game_state = GameState()

        # Verify reset state
        self.assertEqual(self.game_state.score, 0)
        self.assertEqual(len(self.snake.positions), 3)
        self.assert_valid_direction(self.snake.direction)

    def test_direction_change(self):
        """Test direction change handling."""
        # Test valid direction changes
        self.snake.direction = RIGHT
        handle_direction_change(K_UP, self.snake)
        self.assertEqual(self.snake.direction, UP)

        handle_direction_change(K_DOWN, self.snake)
        self.assertEqual(self.snake.direction, UP)  # Should not change to opposite direction

    def test_game_state_update(self):
        """Test game state updates."""
        # Create a snake at a specific position
        self.snake = Snake()
        self.snake.positions = [(5, 5), (4, 5), (3, 5)]  # Snake facing right
        self.snake.direction = RIGHT
        self.snake.length = 3
        self.game_state = GameState()

        # Create a food item right in front of the snake
        food_pos = (6, 5)
        food_type = "normal"
        food_item = self.food._create_food_item(food_pos)
        food_item.type = food_type
        food_item.properties = FOOD_TYPES[food_type]  # Use predefined food properties
        self.food.foods = [food_item]

        # Get initial score
        initial_score = self.game_state.score
        print(f"\nInitial snake head: {self.snake.positions[0]}")
        print(f"Food position: {food_pos}")
        print(f"Initial score: {initial_score}")

        # Update game state (this will also update snake position)
        update_game_state(self.snake, self.obstacles, self.food, self.sound_manager, self.game_state)  # Handle food collision
        print(f"After game state update snake head: {self.snake.positions[0]}")
        print(f"Final score: {self.game_state.score}")

        # Verify food collection
        self.assertTrue(self.game_state.score > initial_score)

    def test_speed_effects(self):
        """Test speed-related food effects."""
        # Test speed boost food
        self.snake = self.create_test_snake_at((5, 5), RIGHT)
        initial_speed = self.snake.speed
        self.game_state = GameState()

        # Create speed boost food in snake's path
        self.food.foods = [self.food._create_food_item((6, 5))]
        self.food.foods[0].type = "speed"
        self.food.foods[0].properties = FOOD_TYPES["speed"]

        # Update game state and verify speed increase
        update_game_state(self.snake, self.obstacles, self.food, self.sound_manager, self.game_state)
        self.assertEqual(self.snake.speed, initial_speed + 2)

        # Test slow down food
        self.snake = self.create_test_snake_at((5, 5), RIGHT)
        initial_speed = self.snake.speed
        self.game_state = GameState()

        # Create slow down food in snake's path
        self.food.foods = [self.food._create_food_item((6, 5))]
        self.food.foods[0].type = "slow"
        self.food.foods[0].properties = FOOD_TYPES["slow"]

        # Update game state and verify speed decrease
        update_game_state(self.snake, self.obstacles, self.food, self.sound_manager, self.game_state)
        self.assertEqual(self.snake.speed, initial_speed - 2)


@pytest.fixture
def setup_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    snake = Snake()
    obstacles = Obstacle()
    food = Food(obstacles)
    game_state = GameState()
    return snake, food, obstacles, screen, game_state


def test_food_creation(setup_game):
    """Test that food items are created with correct properties"""
    _, food, _, _, _ = setup_game

    # Check initial food count
    assert len(food.foods) == 3

    # Check that all foods have valid positions and properties
    for food_item in food.foods:
        assert 0 <= food_item.position[0] < 20  # GRID_WIDTH
        assert 0 <= food_item.position[1] < 15  # GRID_HEIGHT
        assert food_item.type in ["normal", "golden", "speed", "slow"]
        assert food_item.properties == FOOD_TYPES[food_item.type]


def test_food_colors(setup_game):
    """Test that food items have correct colors"""
    _, food, _, _, _ = setup_game

    color_map = {
        "normal": NORMAL_FOOD_COLOR,
        "golden": GOLDEN_APPLE_COLOR,
        "speed": SPEED_FRUIT_COLOR,
        "slow": SLOW_FRUIT_COLOR,
    }

    for food_item in food.foods:
        assert food_item.color == color_map[food_item.type]


def test_food_collision_effects(setup_game):
    """Test that food collision triggers correct effects"""
    snake, food, obstacles, _, game_state = setup_game

    # Mock sound manager
    class MockSoundManager:
        def play_eat_sound(self):
            pass

        def play_crash_sound(self):
            pass

    sound_manager = MockSoundManager()

    # Test each food type
    for food_type in ["normal", "golden", "speed", "slow"]:
        # Reset snake speed to initial value
        snake.speed = 6
        game_state.score = 0  # Reset score
        initial_speed = snake.speed
        print(f"\nTesting {food_type} food:")
        print(f"Initial speed: {initial_speed}")

        # Create a specific food item
        food_pos = (6, 5)  # Place food one step ahead
        food_item = food._create_food_item(food_pos)
        food_item.type = food_type
        food_item.properties = FOOD_TYPES[food_type]
        food.foods = [food_item]

        # Set snake position to move into food
        snake.positions = [(5, 5)]
        snake.direction = RIGHT
        snake.length = 1  # Set length to 1 to avoid self-collision

        # Simulate collision and update game state
        update_game_state(snake, obstacles, food, sound_manager, game_state)
        print(f"Speed after effect: {snake.speed}")
        print(f"Score: {game_state.score}")
        print(f"Snake positions: {snake.positions}")

        if food_type == "normal":
            assert snake.speed == initial_speed
            assert game_state.score == 1  # Normal food gives 1 point
        elif food_type == "golden":
            assert game_state.score == 2  # Golden food gives 2 points
        elif food_type == "speed":
            assert snake.speed > initial_speed
            assert game_state.score == 1  # Speed food gives 1 point
        elif food_type == "slow":
            assert snake.speed < initial_speed
            assert game_state.score == 1  # Slow food gives 1 point


def test_particle_effects(setup_game):
    """Test that particle effects are created on food collision"""
    _, food, _, screen, _ = setup_game

    # Create a food item and trigger collision
    food_pos = (5, 5)
    food_item = food._create_food_item(food_pos)
    food.foods = [food_item]

    # Check initial particle count
    assert len(food.particle_system.particles) == 0

    # Trigger collision and check particles
    food.check_collision(food_pos)

    # Verify particles were created
    assert len(food.particle_system.particles) > 0

    # Test particle rendering
    food.particle_system.render(screen)

    # Store initial particle count
    initial_count = len(food.particle_system.particles)

    # Simulate enough time for particles to expire
    current_time = pygame.time.get_ticks()
    for particle in food.particle_system.particles:
        particle.birth_time = current_time - 2000  # Set birth time to 2 seconds ago

    # Update particles and verify they are removed
    food.particle_system.update()
    assert len(food.particle_system.particles) < initial_count


def test_food_emoji_assignment(setup_game):
    """Test that food items are assigned correct emojis"""
    _, food, _, _, _ = setup_game

    emoji_categories = {
        "normal": ["🍕", "🍇", "🍪", "🍓"],
        "golden": ["🌟", "⭐", "🌞"],
        "speed": ["⚡", "🚀", "💨"],
        "slow": ["🐌", "🦥", "🐢"],
    }

    for food_item in food.foods:
        assert food_item.emoji in emoji_categories[food_item.type]


def test_food_distribution(setup_game):
    """Test the distribution of food types"""
    _, food, _, _, _ = setup_game

    # Create many food items to test probability distribution
    food_types = {"normal": 0, "golden": 0, "speed": 0, "slow": 0}
    samples = 1000

    for _ in range(samples):
        food_item = food._create_food_item((0, 0))
        food_types[food_item.type] += 1

    # Check approximate distributions
    assert 0.55 <= food_types["normal"] / samples <= 0.65  # ~60%
    assert 0.10 <= food_types["golden"] / samples <= 0.20  # ~15%
    assert 0.10 <= food_types["speed"] / samples <= 0.15  # ~12.5%
    assert 0.10 <= food_types["slow"] / samples <= 0.15  # ~12.5%

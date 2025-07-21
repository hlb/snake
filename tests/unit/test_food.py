import pygame
from tests.test_base import SnakeGameTest
from src import Food


class TestFood(SnakeGameTest):
    """Unit tests for Food class functionality."""

    def test_food_initialization(self):
        """Test food initialization and properties."""
        self.assertEqual(len(self.food.foods), 3)
        for food_item in self.food.foods:
            self.assert_position_in_grid(food_item.position)
            self.assertNotIn(food_item.position, self.obstacles.positions)
            self.assertIn(food_item.type, ["normal", "golden", "speed", "slow", "ghost"])
            self.assertIn("points", food_item.properties)

    def test_food_effects(self):
        """Test different food effects on snake."""
        # Test speed fruit effect
        initial_speed = self.snake.speed
        self.snake.handle_food_effect({"points": 1, "speed_change": 2, "duration": 1})
        self.assertEqual(self.snake.speed, initial_speed + 2)
        pygame.time.wait(10)
        self.snake.update(self.obstacles)
        self.assertEqual(self.snake.speed, initial_speed)

        # Test slow fruit effect
        initial_speed = self.snake.speed
        self.snake.handle_food_effect({"points": 1, "speed_change": -2, "duration": 1})
        self.assertEqual(self.snake.speed, initial_speed - 2)
        pygame.time.wait(10)
        self.snake.update(self.obstacles)
        self.assertEqual(self.snake.speed, initial_speed)

    def test_food_position_randomization(self):
        """Test that food positions are properly randomized."""
        # Get initial food positions
        initial_positions = {food.position for food in self.food.foods}

        # Force food regeneration
        new_food = Food(self.obstacles)

        # Get new positions
        new_positions = {food.position for food in new_food.foods}

        # Verify that at least some positions are different
        self.assertTrue(initial_positions != new_positions)

    def test_ghost_food_spawning(self):
        """Test that ghost food can spawn with correct properties."""
        # Create many food items to increase chance of getting ghost food
        ghost_foods = []
        for _ in range(100):  # Create enough instances to likely get ghost food
            food = Food(self.obstacles)
            for food_item in food.foods:
                if food_item.type == "ghost":
                    ghost_foods.append(food_item)
        
        # Should have found at least one ghost food in 100 attempts
        self.assertGreater(len(ghost_foods), 0, "Ghost food should spawn occasionally")
        
        # Test ghost food properties
        ghost_food = ghost_foods[0]
        self.assertEqual(ghost_food.type, "ghost")
        self.assertEqual(ghost_food.properties["points"], 1)
        self.assertEqual(ghost_food.properties["duration"], 8000)  # 8 seconds
        self.assertEqual(ghost_food.emoji, "👻")

    def test_food_type_collision_returns_type(self):
        """Test that food collision returns food type information."""
        # Create a specific ghost food
        ghost_position = (10, 10)
        food = Food(self.obstacles)
        
        # Manually create a ghost food item
        from src.food import FoodItem
        from src.constants import FOOD_TYPES, GHOST_FOOD_COLOR
        from pygame_emojis import load_emoji
        ghost_properties = FOOD_TYPES["ghost"]
        emoji_surface = load_emoji("👻", (36, 36))
        ghost_food = FoodItem(ghost_position, "ghost", GHOST_FOOD_COLOR, 
                             ghost_properties, "👻", emoji_surface)
        
        # Replace one food item with ghost
        food.foods[0] = ghost_food
        
        # Test collision detection
        properties = food.check_collision(ghost_position)
        self.assertIsNotNone(properties)
        self.assertEqual(properties["food_type"], "ghost")

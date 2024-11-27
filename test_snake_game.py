import unittest
import pygame
from src import (
    Snake, Food, Obstacle,
    GRID_WIDTH, GRID_HEIGHT, UP, DOWN, LEFT, RIGHT
)
from snake_game import (
    reset_game, handle_direction_change, update_game_state
)

class TestSnakeGame(unittest.TestCase):
    def setUp(self):
        # Initialize Pygame as it's required for the game
        pygame.init()
        # Create a test display surface
        self.screen = pygame.display.set_mode((800, 600))
        # Create obstacles instance for testing
        self.obstacles = Obstacle()
        
    def test_snake_initial_state(self):
        snake = Snake()
        # Test initial length
        self.assertEqual(len(snake.positions), 3)
        # Test that all positions are within grid
        for pos in snake.positions:
            self.assertTrue(0 <= pos[0] < GRID_WIDTH)
            self.assertTrue(0 <= pos[1] < GRID_HEIGHT)
        # Test initial direction is valid
        self.assertIn(snake.direction, [UP, DOWN, LEFT, RIGHT])
        # Test initial score
        self.assertEqual(snake.score, 0)

    def test_snake_movement(self):
        snake = Snake()
        # Set initial position and direction
        snake.positions = [(10, 10)]
        snake.direction = RIGHT
        initial_head = snake.get_head_position()
        
        # Move snake
        snake.update(self.obstacles)
        new_head = snake.get_head_position()
        
        # Test horizontal movement
        self.assertEqual(new_head[0], (initial_head[0] + 1) % GRID_WIDTH)
        self.assertEqual(new_head[1], initial_head[1])

    def test_snake_collision_with_self(self):
        snake = Snake()
        # Force snake to collide with itself
        snake.positions = [(6, 5), (5, 5), (4, 5)]  # Snake moving right
        snake.direction = LEFT  # Moving left will cause collision with body
        # Should return True for collision
        self.assertTrue(snake.update(self.obstacles))

    def test_food_initialization(self):
        """Test that food is initialized correctly."""
        food = Food(self.obstacles)
        self.assertEqual(len(food.foods), 3)  # Default max_foods is 3
        for food_item in food.foods:
            self.assertTrue(0 <= food_item.position[0] < GRID_WIDTH)
            self.assertTrue(0 <= food_item.position[1] < GRID_HEIGHT)
            self.assertNotIn(food_item.position, self.obstacles.positions)

    def test_food_randomize_position(self):
        """Test that food position can be randomized."""
        food = Food(self.obstacles, max_foods=1)
        initial_pos = food.foods[0].position
        
        # Add obstacle at current food position
        self.obstacles.positions.add(initial_pos)
        
        # Create new food, should be in different position
        new_food = Food(self.obstacles, max_foods=1)
        self.assertNotEqual(initial_pos, new_food.foods[0].position)

    def test_food_types_and_properties(self):
        """Test that food types are correctly initialized with proper properties"""
        food = Food(self.obstacles)
        for food_item in food.foods:
            self.assertIn(food_item.type, ['normal', 'golden', 'speed'])
            self.assertIsNotNone(food_item.properties)
            self.assertIn('points', food_item.properties)
            self.assertIn('speed_change', food_item.properties)
            self.assertIn('duration', food_item.properties)

    def test_golden_apple_effect(self):
        """Test that golden apple gives correct score"""
        snake = Snake()
        food = Food(self.obstacles)
        
        # Create a golden apple
        golden_properties = {
            'points': 2,
            'speed_change': 0,
            'duration': 0
        }
        
        # Apply effect
        initial_score = snake.score
        snake.handle_food_effect(golden_properties)
        
        # Check that score increased by 2
        self.assertEqual(snake.score, initial_score + 2)

    def test_speed_fruit_effect(self):
        """Test that speed fruit correctly affects snake speed"""
        snake = Snake()
        initial_speed = snake.speed
        
        # Create speed fruit properties
        speed_properties = {
            'points': 1,
            'speed_change': 2,
            'duration': 5000
        }
        
        # Apply effect
        snake.handle_food_effect(speed_properties)
        
        # Check that speed increased
        self.assertEqual(snake.speed, initial_speed + 2)
        self.assertTrue(snake.effect_end_time > 0)

    def test_speed_effect_expiration(self):
        """Test that speed effect correctly expires"""
        snake = Snake()
        initial_speed = snake.speed
        
        # Create speed fruit properties with very short duration
        speed_properties = {
            'points': 1,
            'speed_change': 2,
            'duration': 1  # 1ms duration
        }
        
        # Apply effect
        snake.handle_food_effect(speed_properties)
        
        # Wait for effect to expire
        pygame.time.wait(10)  # Wait 10ms
        
        # Update to trigger effect expiration
        snake.update(self.obstacles)
        
        # Test that speed returned to normal
        self.assertEqual(snake.speed, initial_speed)

    def test_obstacle_initialization(self):
        obstacles = Obstacle()
        # Test that obstacles are created
        self.assertTrue(len(obstacles.positions) > 0)
        # Test that all obstacles are within grid
        for pos in obstacles.positions:
            self.assertTrue(0 <= pos[0] < GRID_WIDTH)
            self.assertTrue(0 <= pos[1] < GRID_HEIGHT)

    def test_snake_collision_with_obstacle(self):
        snake = Snake()
        # Force snake to be at a specific position
        snake.positions = [(5, 5)]
        # Add obstacle at snake's next position
        self.obstacles.positions = {(6, 5)}
        snake.direction = RIGHT
        # Should return True for collision
        self.assertTrue(snake.update(self.obstacles))

    def test_snake_growth(self):
        """Test that snake grows correctly when eating food"""
        snake = Snake()
        food = Food(self.obstacles)
        initial_length = len(snake.positions)
        
        # Simulate eating food
        snake.length += 1  # Increase length directly
        snake.update(self.obstacles)  # Update to apply growth
        
        # Test that snake grew
        self.assertEqual(len(snake.positions), initial_length + 1)

    def test_snake_no_collision_on_start(self):
        """Test that snake doesn't collide with anything when game starts"""
        snake = Snake()
        # Test initial movement without any obstacles
        self.assertFalse(snake.update(Obstacle()))
        
    def test_snake_valid_movement_sequence(self):
        """Test that snake can move freely without collisions in valid scenarios"""
        snake = Snake()
        obstacles = Obstacle()
        # Clear any random obstacles to ensure clean test
        obstacles.positions.clear()
        
        # Set initial position and direction
        snake.positions = [(5, 5), (4, 5), (3, 5)]  # Snake facing right
        
        # Move snake in a square pattern
        movements = [RIGHT, DOWN, LEFT, UP]
        for direction in movements:
            snake.direction = direction
            # Should return False for no collision
            self.assertFalse(snake.update(obstacles))
            
    def test_snake_collision_detection_accuracy(self):
        """Test that collision detection works accurately in various scenarios"""
        snake = Snake()
        obstacles = Obstacle()
        obstacles.positions.clear()  # Clear random obstacles
        
        # Test case 1: No collision when moving in empty space
        snake.positions = [(5, 5), (4, 5), (3, 5)]  # Snake facing right
        snake.direction = RIGHT
        self.assertFalse(snake.update(obstacles))
        
        # Test case 2: Collision with obstacle directly in front
        snake.positions = [(5, 5), (4, 5), (3, 5)]  # Reset position
        obstacles.positions.add((6, 5))  # Place obstacle in front
        snake.direction = RIGHT
        self.assertTrue(snake.update(obstacles))
        
        # Test case 3: Collision with own body when turning back
        snake.positions = [(5, 5), (4, 5), (3, 5)]  # Reset position
        obstacles.positions.clear()  # Clear obstacles
        snake.direction = LEFT  # Turn back into body
        self.assertTrue(snake.update(obstacles))

    def test_start_menu_rendering(self):
        """Test that start menu renders correctly"""
        from snake_game import show_start_menu
        
        # Create a test surface
        test_surface = pygame.Surface((800, 600))
        
        # Should not raise any exceptions
        try:
            show_start_menu(test_surface)
            rendered = True
        except Exception as e:
            rendered = False
        
        self.assertTrue(rendered, "Start menu should render without errors")
        
        # Test that the surface has been modified (not empty/black)
        self.assertGreater(
            pygame.transform.average_color(test_surface)[0], 0,
            "Start menu should render content on the surface"
        )

    def test_game_state_transitions(self):
        """Test game state transitions from menu to game"""
        from snake_game import main
        
        # Create a mock event for RETURN key press
        start_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})
        pygame.event.post(start_event)
        
        # Create a mock event for game quit
        quit_event = pygame.event.Event(pygame.QUIT)
        pygame.event.post(quit_event)
        
        # Should not raise any exceptions
        try:
            main()  # Will exit immediately due to quit event
            transitioned = True
        except Exception as e:
            transitioned = False
        
        self.assertTrue(transitioned, "Game should handle state transitions without errors")

    def test_key_event_handling(self):
        """Test that key events are handled correctly in different game states"""
        from snake_game import main
        
        # Test sequence of events
        test_events = [
            pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN}),  # Start game
            pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}),      # Move up
            pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE}),   # Restart
            pygame.event.Event(pygame.QUIT)                                # Quit
        ]
        
        # Post all test events
        for event in test_events:
            pygame.event.post(event)
        
        # Should handle all events without errors
        try:
            main()  # Will exit due to quit event
            handled = True
        except Exception as e:
            handled = False
        
        self.assertTrue(handled, "Game should handle all key events correctly")

    def test_game_reset(self):
        """Test that game reset function properly initializes all components"""
        snake, obstacles, food = reset_game()
        
        # Test snake initialization
        self.assertIsInstance(snake, Snake)
        self.assertEqual(len(snake.positions), 3)
        self.assertEqual(snake.score, 0)
        
        # Test obstacles initialization
        self.assertIsInstance(obstacles, Obstacle)
        self.assertTrue(len(obstacles.positions) > 0)
        
        # Test food initialization
        self.assertIsInstance(food, Food)
        self.assertEqual(len(food.foods), 3)  # Default max_foods is 3
        for food_item in food.foods:
            self.assertTrue(0 <= food_item.position[0] < GRID_WIDTH)
            self.assertTrue(0 <= food_item.position[1] < GRID_HEIGHT)

    def test_direction_change_handling(self):
        """Test that direction changes are handled correctly"""
        snake = Snake()
        original_direction = snake.direction
        
        # Test valid direction change
        if original_direction != (0, 1):  # If not moving down
            handle_direction_change(pygame.K_UP, snake)
            self.assertEqual(snake.direction, (0, -1))
        
        # Test invalid direction change (trying to move in opposite direction)
        current_direction = snake.direction
        invalid_directions = {
            (0, -1): pygame.K_DOWN,   # UP -> DOWN
            (0, 1): pygame.K_UP,      # DOWN -> UP
            (-1, 0): pygame.K_RIGHT,  # LEFT -> RIGHT
            (1, 0): pygame.K_LEFT     # RIGHT -> LEFT
        }
        if current_direction in invalid_directions:
            handle_direction_change(invalid_directions[current_direction], snake)
            self.assertEqual(snake.direction, current_direction)

    def test_update_game_state(self):
        """Test that game state updates correctly"""
        snake = Snake()
        obstacles = Obstacle()
        food = Food(obstacles, max_foods=1)  # Use single food for simpler testing
        
        # Test normal movement (no collision)
        snake.positions = [(5, 5), (4, 5), (3, 5)]
        snake.direction = (1, 0)  # Moving right
        obstacles.positions = {(7, 5)}  # Obstacle away from snake
        food.foods[0] = food._create_food_item((8, 5))  # Food away from snake
        
        game_over = update_game_state(snake, obstacles, food)
        self.assertFalse(game_over)
        
        # Test collision with obstacle
        snake.positions = [(6, 5), (5, 5), (4, 5)]
        snake.direction = (1, 0)  # Moving right
        obstacles.positions = {(7, 5)}  # Obstacle in snake's path
        
        game_over = update_game_state(snake, obstacles, food)
        self.assertTrue(game_over)
        
        # Test eating food
        snake = Snake()
        initial_length = snake.length
        initial_score = snake.score
        snake.positions = [(4, 5), (3, 5), (2, 5)]
        snake.direction = (1, 0)  # Moving right
        food.foods[0] = food._create_food_item((5, 5))  # Food in snake's path
        obstacles.positions = {(7, 5)}  # Obstacle away from snake
        
        game_over = update_game_state(snake, obstacles, food)
        self.assertFalse(game_over)
        self.assertGreater(snake.length, initial_length)
        self.assertGreater(snake.score, initial_score)

    def test_multiple_food_items(self):
        """Test that multiple food items work correctly"""
        # Initialize with 3 food items
        food = Food(self.obstacles, max_foods=3)
        
        # Check that we have correct number of food items
        self.assertEqual(len(food.foods), 3)
        
        # Check that all food positions are unique
        positions = [food_item.position for food_item in food.foods]
        self.assertEqual(len(positions), len(set(positions)))
        
        # Check that removing food works correctly
        first_food_pos = food.foods[0].position
        properties = food.remove_food(first_food_pos)
        
        # Verify properties were returned
        self.assertIsNotNone(properties)
        self.assertIn('points', properties)
        self.assertIn('speed_change', properties)
        self.assertIn('duration', properties)
        
        # Check that a new food item was created
        self.assertEqual(len(food.foods), 3)
        
        # Check that the new food position is different
        self.assertNotIn(first_food_pos, [food_item.position for food_item in food.foods])

    def test_snake_food_interaction(self):
        """Test that snake correctly interacts with multiple food items"""
        food = Food(self.obstacles, max_foods=1)  # Use single food for simpler testing
        snake = Snake()
        
        # Position snake one space away from food
        food_pos = food.foods[0].position
        snake.positions = [
            ((food_pos[0] - 1) % GRID_WIDTH, food_pos[1])  # One space to the left of food
        ]
        snake.direction = RIGHT  # Moving right towards food
        
        # Store initial score
        initial_score = snake.score
        
        # First update - snake should eat the food
        game_over = update_game_state(snake, self.obstacles, food)
        
        # Verify food was eaten and score increased
        self.assertFalse(game_over)
        self.assertGreater(snake.score, initial_score)
        self.assertEqual(len(food.foods), 1)  # Should still have one food
        self.assertNotEqual(food.foods[0].position, food_pos)  # New food should be in different position
        
        # Get new food position
        new_food_pos = food.foods[0].position
        self.assertNotEqual(new_food_pos, food_pos)  # Verify positions are different

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()

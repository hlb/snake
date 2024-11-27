import unittest
import pygame
from src import (
    Snake, Food, Obstacle,
    GRID_WIDTH, GRID_HEIGHT, UP, DOWN, LEFT, RIGHT
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
        initial_head = snake.get_head_position()
        snake.direction = RIGHT
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
        food = Food(self.obstacles)
        # Test that food position is within grid
        self.assertTrue(0 <= food.position[0] < GRID_WIDTH)
        self.assertTrue(0 <= food.position[1] < GRID_HEIGHT)
        # Test that food has an emoji
        self.assertTrue(hasattr(food, 'emoji'))
        self.assertTrue(hasattr(food, 'emoji_surface'))

    def test_food_randomize_position(self):
        food = Food(self.obstacles)
        initial_pos = food.position
        initial_emoji = food.emoji
        food.randomize_position()
        # Test that either position or emoji has changed
        different_pos = initial_pos != food.position
        different_emoji = initial_emoji != food.emoji
        self.assertTrue(different_pos or different_emoji)

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

    def test_food_types_and_properties(self):
        """Test that food types are correctly initialized with proper properties"""
        food = Food(self.obstacles)
        
        # Test that food type is one of the expected types
        self.assertIn(food.type, ['normal', 'golden', 'speed'])
        
        # Test that food has correct properties based on type
        self.assertIsNotNone(food.properties)
        self.assertIn('points', food.properties)
        self.assertIn('speed_change', food.properties)
        self.assertIn('duration', food.properties)
        
        # Test that food has correct emoji based on type
        self.assertIn(food.emoji, food.food_emojis[food.type])

    def test_golden_apple_effect(self):
        """Test that golden apple gives correct score"""
        snake = Snake()
        food = Food(self.obstacles)
        
        # Force food to be golden apple
        food.type = 'golden'
        food.properties = {'points': 2, 'speed_change': 0, 'duration': 0}
        
        # Simulate eating golden apple
        initial_score = snake.score
        snake.handle_food_effect(food)
        
        # Test score increase
        self.assertEqual(snake.score, initial_score + 2)

    def test_speed_fruit_effect(self):
        """Test that speed fruit correctly affects snake speed"""
        snake = Snake()
        food = Food(self.obstacles)
        
        # Force food to be speed fruit
        food.type = 'speed'
        food.properties = {'points': 1, 'speed_change': 2, 'duration': 5000}
        
        # Record initial speed
        initial_speed = snake.speed
        
        # Simulate eating speed fruit
        snake.handle_food_effect(food)
        
        # Test immediate speed increase
        self.assertEqual(snake.speed, initial_speed + 2)
        
        # Test that effect end time is set
        self.assertGreater(snake.effect_end_time, pygame.time.get_ticks())

    def test_speed_effect_expiration(self):
        """Test that speed effect correctly expires"""
        snake = Snake()
        food = Food(self.obstacles)
        
        # Force food to be speed fruit with very short duration
        food.type = 'speed'
        food.properties = {'points': 1, 'speed_change': 2, 'duration': 100}
        
        # Record initial speed
        initial_speed = snake.speed
        
        # Simulate eating speed fruit
        snake.handle_food_effect(food)
        
        # Wait for effect to expire
        pygame.time.wait(200)
        
        # Update snake to trigger effect expiration check
        snake.update(self.obstacles)
        
        # Test that speed returned to normal
        self.assertEqual(snake.speed, initial_speed)

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()

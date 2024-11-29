import unittest.mock
import pytest
import pygame
from snake_game import handle_direction_change, update_game_state
from src.snake import Snake
from src.food import Food
from src.obstacle import Obstacle
from src.sound import SoundManager


# pylint: disable=redefined-outer-name
@pytest.fixture
def snake():
    return Snake()


@pytest.fixture
def obstacles():
    return Obstacle()


@pytest.fixture
def food(obstacles):
    return Food(obstacles)


@pytest.fixture
def sound_manager():
    return unittest.mock.Mock(spec=SoundManager)


class TestHandleDirectionChange:
    def test_valid_direction_changes(self, snake):
        # Test all valid direction changes
        test_cases = [(pygame.K_UP, (0, -1)), (pygame.K_DOWN, (0, 1)), (pygame.K_LEFT, (-1, 0)), (pygame.K_RIGHT, (1, 0))]
        for key, expected_direction in test_cases:
            snake.direction = (0, 0)  # Reset direction
            handle_direction_change(key, snake)
            assert snake.direction == expected_direction

    def test_invalid_direction_changes(self, snake):
        # Test that snake can't reverse direction
        test_cases = [((0, -1), pygame.K_DOWN), ((0, 1), pygame.K_UP), ((-1, 0), pygame.K_RIGHT), ((1, 0), pygame.K_LEFT)]
        for initial_direction, key in test_cases:
            snake.direction = initial_direction
            handle_direction_change(key, snake)
            assert snake.direction == initial_direction


class TestUpdateGameState:
    def test_collision_with_obstacle(self, snake, obstacles, food, sound_manager):
        # Mock snake.update to return True (collision)
        snake.update = unittest.mock.Mock(return_value=True)
        game_over = update_game_state(snake, obstacles, food, sound_manager)
        assert game_over is True
        sound_manager.play_crash_sound.assert_called_once()

    def test_eating_food(self, snake, obstacles, food, sound_manager):
        # Mock collision detection
        initial_length = snake.length
        initial_score = snake.score
        food_properties = {"points": 1, "speed_change": 0, "duration": 0}
        food.check_collision = unittest.mock.Mock(return_value=food_properties)
        snake.update = unittest.mock.Mock(return_value=False)
        game_over = update_game_state(snake, obstacles, food, sound_manager)
        assert game_over is False
        assert snake.length == initial_length + 1
        assert snake.score == initial_score + 1
        sound_manager.play_eat_sound.assert_called_once()

    def test_screenshot_on_food_collection(self, snake, obstacles, food, sound_manager):
        # Mock collision detection
        food_properties = {"points": 1, "speed_change": 0, "duration": 0}
        food.check_collision = unittest.mock.Mock(return_value=food_properties)
        snake.update = unittest.mock.Mock(return_value=False)
        screenshot_manager = unittest.mock.Mock()
        update_game_state(snake, obstacles, food, sound_manager, enable_screenshots=True, screenshot_manager=screenshot_manager)
        screenshot_manager.schedule.assert_called_once()

    def test_obstacle_addition_on_score_milestone(self, snake, obstacles, food, sound_manager):
        # Set up score to trigger obstacle addition
        snake.score = 9
        initial_speed = snake.speed
        food_properties = {"points": 1, "speed_change": 0, "duration": 0}  # This will make score 10
        food.check_collision = unittest.mock.Mock(return_value=food_properties)
        snake.update = unittest.mock.Mock(return_value=False)
        obstacles.add_obstacle = unittest.mock.Mock()
        update_game_state(snake, obstacles, food, sound_manager)
        obstacles.add_obstacle.assert_called_once_with(snake)
        assert snake.speed == initial_speed + 1  # Speed should increase

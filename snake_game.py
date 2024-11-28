import os
import argparse
import pygame
from src import (
    Snake,
    Food,
    Obstacle,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)
from src.sound import SoundManager
from src.ui import GameRenderer, Screenshot
from src.game_state import GameState

# Initialize Pygame
pygame.init()


def handle_direction_change(key, snake):
    directions = {
        pygame.K_UP: ((0, -1), (0, 1)),
        pygame.K_DOWN: ((0, 1), (0, -1)),
        pygame.K_LEFT: ((-1, 0), (1, 0)),
        pygame.K_RIGHT: ((1, 0), (-1, 0)),
    }
    if key in directions and snake.direction != directions[key][1]:
        snake.direction = directions[key][0]


def update_game_state(snake, obstacles, food, sound_manager, enable_screenshots=False, screenshot_manager=None):
    """Update game state and handle collisions."""
    # Check for collision with obstacles or self
    if snake.update(obstacles):
        sound_manager.play_crash_sound()
        return True

    # Check for collision with any food
    head_pos = snake.get_head_position()
    food_properties = food.check_collision(head_pos)

    if food_properties:
        sound_manager.play_eat_sound()
        snake.length += food_properties["points"]
        snake.score += food_properties["points"]  # Update score when eating food
        snake.handle_food_effect(food_properties)

        # Schedule screenshot if enabled
        if enable_screenshots and screenshot_manager:
            screenshot_manager.schedule()

        # Add new obstacle every 10 points
        if snake.score % 10 == 0:
            obstacles.add_obstacle(snake)
            snake.speed += 1

    return False


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Snake Game")
    parser.add_argument("--screenshots", action="store_true", help="Enable screenshots when snake eats food")
    args = parser.parse_args()

    # Initialize game components
    game_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Modern Snake Game")
    clock = pygame.time.Clock()

    # Initialize managers
    sound_manager = SoundManager()
    game_state = GameState()
    renderer = GameRenderer()
    screenshot_manager = Screenshot() if args.screenshots else None

    # Start background music
    sound_manager.play_background_music()

    while True:
        if not game_state.is_playing and not game_state.is_game_over:
            renderer.show_start_menu(game_screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return
                    if event.key == pygame.K_RETURN:
                        snake = Snake()
                        obstacles = Obstacle()
                        food = Food(obstacles)
                        game_state.start_game()

        elif game_state.is_game_over:
            renderer.show_game_over(game_screen, game_state.score, game_state.high_score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return
                    if event.key == pygame.K_RETURN:
                        snake = Snake()
                        obstacles = Obstacle()
                        food = Food(obstacles)
                        game_state.start_game()

        else:  # Game is running
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return
                    handle_direction_change(event.key, snake)

            # Update game state
            game_over = update_game_state(snake, obstacles, food, sound_manager, enable_screenshots=args.screenshots, screenshot_manager=screenshot_manager)

            if game_over:
                game_state.end_game()
            else:
                game_state.update_score(snake.score)
                renderer.render_game(game_screen, snake, food, obstacles, game_state.is_game_over, game_state.score, game_state.high_score, screenshot_manager)

            clock.tick(snake.speed)


if __name__ == "__main__":
    main()

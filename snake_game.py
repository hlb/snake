import argparse
import pygame
from src import Snake, Food, Obstacle, WINDOW_WIDTH, WINDOW_HEIGHT
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


def update_game_state(snake, obstacles, food, sound_manager, game_state, enable_screenshots=False, screenshot_manager=None):
    """Update game state and handle collisions."""
    # Check for collision with obstacles or self
    if snake.update(obstacles):
        sound_manager.play_crash_sound()
        return True

    # Check for collision with food
    food_properties = food.check_collision(snake.get_head_position())
    if food_properties:
        sound_manager.play_eat_sound()
        snake.length += food_properties["points"]
        game_state.update_score(game_state.score + food_properties["points"])  # Update score directly in game_state
        snake.handle_food_effect(food_properties)

        # Schedule screenshot if enabled
        if enable_screenshots and screenshot_manager:
            screenshot_manager.schedule()

        # Add new obstacle every 10 points
        if game_state.score % 10 == 0:
            obstacles.add_obstacle(snake)
            snake.speed += 1

    return False


def main():
    # Initialize start_time with current ticks
    game_state = GameState()
    game_state.start_time = pygame.time.get_ticks()

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
    renderer = GameRenderer()
    screenshot_manager = Screenshot() if args.screenshots else None

    # Start background music
    sound_manager.play_background_music()

    # Game objects
    snake = None
    obstacles = None
    food = None

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    return
                if event.key == pygame.K_RETURN and (not game_state.is_playing or game_state.is_game_over):
                    # Start new game
                    snake = Snake()
                    obstacles = Obstacle()
                    food = Food(obstacles)
                    game_state.start_game()
                    game_state.start_time = pygame.time.get_ticks()  # Reset start_time
                if event.key == pygame.K_ESCAPE and game_state.is_playing:
                    game_state.toggle_pause()
                    if game_state.is_paused:
                        sound_manager.pause_background_music()
                    else:
                        sound_manager.resume_background_music()
                if game_state.is_playing and not game_state.is_paused:
                    handle_direction_change(event.key, snake)

        # Update game state
        if game_state.is_playing and not game_state.is_paused:
            if update_game_state(snake, obstacles, food, sound_manager, game_state, args.screenshots, screenshot_manager):
                game_state.end_game()

        # Render current frame
        if game_state.is_playing:
            renderer.render_game(game_screen, snake, food, obstacles, game_state.score, game_state.high_score, game_state.start_time, screenshot_manager)
            if game_state.is_paused:
                renderer.show_pause_menu(game_screen, game_state.score)
        elif game_state.is_game_over:
            renderer.show_game_over(game_screen, game_state.score, game_state.high_score)
        else:  # Game is not started
            renderer.show_start_menu(game_screen)

        # Update display once per frame
        pygame.display.flip()

        # Control game speed
        clock.tick(snake.speed if snake and game_state.is_playing and not game_state.is_paused else 30)


if __name__ == "__main__":
    main()

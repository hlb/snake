import os
import pygame
from src import (
    Snake,
    Food,
    Obstacle,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BACKGROUND,
    SCORE_COLOR,
    GAME_OVER_COLOR,
    get_font,
    draw_grid,
)

# Initialize Pygame
pygame.init()

# Initialize sound system
pygame.mixer.quit()  # First close any running sound system
pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.set_num_channels(8)  # Set more channels


# Load sound effects
def load_sound(file_path):
    if not os.path.exists(file_path):
        print(f"Sound file not found: {file_path}")
        return None
    try:
        sound = pygame.mixer.Sound(file_path)
        print(f"Successfully loaded sound: {file_path}")
        return sound
    except Exception as sound_load_error:
        print(f"Failed to load sound file {file_path}: {str(sound_load_error)}")
        return None


# Set sound effects
eat_sound = load_sound("sounds/eat.wav")
crash_sound = load_sound("sounds/crash.wav")
background_music = load_sound("sounds/background.mp3")

# Set volume
if eat_sound:
    eat_sound.set_volume(0.4)
if crash_sound:
    crash_sound.set_volume(0.3)
if background_music:
    background_music.set_volume(0.8)
    channel = pygame.mixer.Channel(0)
    channel.set_volume(0.8)
    try:
        channel.play(background_music, loops=-1)
        print("Background music started playing")
    except Exception as e:
        print(f"Failed to play background music: {str(e)}")


class GameState:
    def __init__(self):
        self.high_score = self.load_high_score()
        self.start_time = 0

    def load_high_score(self):
        try:
            with open("high_score.txt", "r", encoding="utf-8") as f:
                return int(f.read())
        except FileNotFoundError:
            return 0
        except ValueError:
            return 0

    def save_high_score(self, score):
        with open("high_score.txt", "w", encoding="utf-8") as f:
            f.write(str(score))


# Create game window
game_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Modern Snake Game")
clock = pygame.time.Clock()


def show_start_menu(screen):
    """Show start menu screen"""
    screen.fill(BACKGROUND)
    draw_grid(screen)

    # Title
    font = get_font(64)
    title = font.render("Snake Game", True, GAME_OVER_COLOR)
    title_rect = title.get_rect()
    title_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
    screen.blit(title, title_rect)

    # Start instruction
    font = get_font(32)
    instruction = font.render("Press ENTER to Start", True, SCORE_COLOR)
    instruction_rect = instruction.get_rect()
    instruction_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
    screen.blit(instruction, instruction_rect)

    pygame.display.flip()


def show_game_over(screen, score, game_state):
    """Show game over screen"""
    if score > game_state.high_score:
        game_state.high_score = score
        game_state.save_high_score(game_state.high_score)

    font = get_font(64)
    text = font.render("Game Over!", True, GAME_OVER_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
    screen.blit(text, text_rect)

    font = get_font(32)
    score_text = font.render(f"Score: {score}", True, SCORE_COLOR)
    score_rect = score_text.get_rect()
    score_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
    screen.blit(score_text, score_rect)

    high_score_text = font.render(f"High Score: {game_state.high_score}", True, SCORE_COLOR)
    high_score_rect = high_score_text.get_rect()
    high_score_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    screen.blit(high_score_text, high_score_rect)

    restart_text = font.render("Press ENTER to Restart", True, SCORE_COLOR)
    restart_rect = restart_text.get_rect()
    restart_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()


def handle_direction_change(key, snake):
    directions = {
        pygame.K_UP: ((0, -1), (0, 1)),
        pygame.K_DOWN: ((0, 1), (0, -1)),
        pygame.K_LEFT: ((-1, 0), (1, 0)),
        pygame.K_RIGHT: ((1, 0), (-1, 0)),
    }
    if key in directions and snake.direction != directions[key][1]:
        snake.direction = directions[key][0]


def update_game_state(snake, obstacles, food):
    """Update game state and handle collisions."""
    # Check for collision with obstacles or self
    if snake.update(obstacles):
        if crash_sound:
            crash_sound.play()
        return True

    # Check for collision with any food
    head_pos = snake.get_head_position()
    food_properties = food.check_collision(head_pos)

    if food_properties:
        if eat_sound:
            eat_sound.play()
        snake.length += food_properties["points"]
        snake.score += food_properties["points"]  # Update score when eating food
        snake.handle_food_effect(food_properties)

        # Add new obstacle every 10 points
        if snake.score % 10 == 0:
            obstacles.add_obstacle(snake)
            snake.speed += 1

    return False


def render_game(screen, snake, food, obstacles, game_over, game_state):
    """Render the game state"""
    screen.fill(BACKGROUND)
    draw_grid(screen)

    # Draw game objects
    food.render(screen)
    obstacles.render(screen)
    snake.render(screen)

    # Draw score
    font = get_font(24)
    score_text = font.render(f"Score: {snake.score}", True, SCORE_COLOR)
    screen.blit(score_text, (10, 10))

    # Draw high score
    high_score_text = font.render(f"High Score: {game_state.high_score}", True, SCORE_COLOR)
    high_score_rect = high_score_text.get_rect()
    high_score_rect.topright = (WINDOW_WIDTH - 10, 10)
    screen.blit(high_score_text, high_score_rect)

    # Draw timer
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time // 1000  # Convert to seconds
    time_text = font.render(f"Time: {elapsed_time}s", True, SCORE_COLOR)
    time_rect = time_text.get_rect()
    time_rect.midtop = (WINDOW_WIDTH // 2, 10)
    screen.blit(time_text, time_rect)

    if game_over:
        show_game_over(screen, snake.score, game_state)
    else:
        pygame.display.flip()


def main():
    game_state = GameState()
    snake = Snake()
    obstacles = Obstacle()
    food = Food(obstacles)
    game_over = False
    game_started = False
    game_state.start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    return

                if not game_started:
                    if event.key == pygame.K_RETURN:
                        game_started = True
                        game_state.start_time = pygame.time.get_ticks()  # Reset start time when game starts
                elif game_over:
                    if event.key == pygame.K_RETURN:
                        snake = Snake()
                        food = Food(obstacles)
                        game_over = False
                        game_state.start_time = pygame.time.get_ticks()  # Reset start time on restart
                else:
                    handle_direction_change(event.key, snake)

        if not game_started:
            show_start_menu(game_screen)
            continue

        if not game_over:
            game_over = update_game_state(snake, obstacles, food)

        render_game(game_screen, snake, food, obstacles, game_over, game_state)
        clock.tick(snake.speed)


if __name__ == "__main__":
    main()

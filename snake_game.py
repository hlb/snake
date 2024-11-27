import pygame
import os
from pygame import mixer
from src import (
    Snake, Food, Obstacle,
    WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND, SCORE_COLOR,
    GAME_OVER_COLOR, get_font, draw_grid
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
    except Exception as e:
        print(f"Failed to load sound file {file_path}: {str(e)}")
        return None

# Set sound effects
eat_sound = load_sound('sounds/eat.wav')
crash_sound = load_sound('sounds/crash.wav')
background_music = load_sound('sounds/background.wav')

# Set volume
if eat_sound:
    eat_sound.set_volume(0.4)
if crash_sound:
    crash_sound.set_volume(0.3)
if background_music:
    background_music.set_volume(0.8)  # Increase volume to 0.8
    channel = pygame.mixer.Channel(0)
    channel.set_volume(0.8)  # Increase channel volume to 0.8
    try:
        channel.play(background_music, loops=-1)
        print("Background music started playing")
    except Exception as e:
        print(f"Failed to play background music: {str(e)}")

# Create game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Modern Snake Game')
clock = pygame.time.Clock()

def show_game_over(screen, score):
    """Show game over screen"""
    font = get_font(64)
    text = font.render('Game Over!', True, GAME_OVER_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
    screen.blit(text, text_rect)
    
    font = get_font(32)
    score_text = font.render(f'Score: {score}', True, SCORE_COLOR)
    score_rect = score_text.get_rect()
    score_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
    screen.blit(score_text, score_rect)
    
    pygame.display.flip()

def show_start_menu(screen):
    """Show start menu screen"""
    screen.fill(BACKGROUND)
    draw_grid(screen)
    
    # Title
    font = get_font(64)
    title = font.render('Snake Game', True, GAME_OVER_COLOR)
    title_rect = title.get_rect()
    title_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
    screen.blit(title, title_rect)
    
    # Start instruction
    font = get_font(32)
    instruction = font.render('Press ENTER to Start', True, SCORE_COLOR)
    instruction_rect = instruction.get_rect()
    instruction_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
    screen.blit(instruction, instruction_rect)
    
    pygame.display.flip()

def main():
    snake = Snake()
    obstacles = Obstacle()
    food = Food(obstacles)
    game_over = False
    game_started = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if not game_started:
                    if event.key == pygame.K_RETURN:  # Enter key
                        game_started = True
                        continue
                elif game_over:
                    if event.key == pygame.K_SPACE:
                        # Reset game
                        snake = Snake()
                        obstacles = Obstacle()
                        food = Food(obstacles)
                        game_over = False
                        continue
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        return
                else:
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)
        
        if not game_started:
            show_start_menu(screen)
            continue
            
        if not game_over:
            # Update snake position
            collision = snake.update(obstacles)
            if collision:
                if crash_sound:
                    crash_sound.play()
                game_over = True
                continue
            
            # Check if snake ate food
            if snake.get_head_position() == food.position:
                if eat_sound:
                    eat_sound.play()
                snake.length += 1
                snake.score += 1
                food.randomize_position()
                # Add new obstacle every 10 points
                if snake.score % 10 == 0:
                    obstacles.add_obstacle(snake)
                    snake.speed += 1  # Increase speed
        
        # Draw everything
        screen.fill(BACKGROUND)
        draw_grid(screen)
        snake.render(screen)
        food.render(screen)
        obstacles.render(screen)
        
        # Draw score
        font = get_font(24)
        score_text = font.render(f'Score: {snake.score}', True, SCORE_COLOR)
        screen.blit(score_text, (10, 10))
        
        if game_over:
            show_game_over(screen, snake.score)
        
        pygame.display.flip()
        clock.tick(snake.speed)

if __name__ == '__main__':
    main()

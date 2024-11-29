import os
from datetime import datetime
import pygame

from . import WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND, SCORE_COLOR, GAME_OVER_COLOR, get_font, draw_grid


class Screenshot:
    delay_ms = 500

    def __init__(self):
        self.pending = False
        self.scheduled_time = 0
        self.directory = "screenshots"
        os.makedirs(self.directory, exist_ok=True)

    def schedule(self):
        """Schedule a screenshot to be taken after delay_ms"""
        self.pending = True
        self.scheduled_time = pygame.time.get_ticks() + self.delay_ms

    def update(self, screen):
        """Check and take screenshot if scheduled time has passed"""
        if not self.pending:
            return

        current_time = pygame.time.get_ticks()
        if current_time >= self.scheduled_time:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"{self.directory}/snake_{timestamp}.png"
            pygame.image.save(screen, path)
            self.pending = False


class GameRenderer:
    @staticmethod
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

    @staticmethod
    def show_game_over(screen, score, high_score):
        """Show game over screen"""
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

        high_score_text = font.render(f"High Score: {high_score}", True, SCORE_COLOR)
        high_score_rect = high_score_text.get_rect()
        high_score_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        screen.blit(high_score_text, high_score_rect)

        restart_text = font.render("Press ENTER to Restart", True, SCORE_COLOR)
        restart_rect = restart_text.get_rect()
        restart_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)
        screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    @staticmethod
    def render_game(screen, snake, food, obstacles, score, high_score, screenshot_manager=None):
        """Render the game screen with all components."""
        screen.fill(BACKGROUND)
        draw_grid(screen)

        # Render game objects
        snake.render(screen)
        food.render(screen)
        obstacles.render(screen)

        # Draw scores
        score_text = get_font(24).render(f"Score: {score}", True, SCORE_COLOR)
        high_score_text = get_font(24).render(f"High Score: {high_score}", True, SCORE_COLOR)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (WINDOW_WIDTH - high_score_text.get_width() - 10, 10))

        if screenshot_manager:
            screenshot_manager.update(screen)

        pygame.display.flip()

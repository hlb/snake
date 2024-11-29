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
    def __init__(self):
        """Initialize the game renderer with a cached background"""
        self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background.fill(BACKGROUND)
        draw_grid(self.background)

    def render_text(self, screen, text, color, position, size=32, align="center"):
        """Render text with specified alignment (center, left, or right)."""
        font = get_font(size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if align == "center":
            text_rect.center = position
        elif align == "right":
            text_rect.topright = position
        else:  # left align
            text_rect.topleft = position

        screen.blit(text_surface, text_rect)

    def show_start_menu(self, screen):
        """Show start menu screen"""
        screen.blit(self.background, (0, 0))

        # Title
        self.render_text(screen, "Snake Game", GAME_OVER_COLOR, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50), 64, align="center")

        # Start instruction
        self.render_text(screen, "Press ENTER to Start", SCORE_COLOR, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50), align="center")

    def show_game_over(self, screen, score, high_score):
        """Show game over screen"""
        screen.blit(self.background, (0, 0))

        # Game Over text
        self.render_text(screen, "Game Over!", GAME_OVER_COLOR, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50), 64, align="center")

        # Score texts
        self.render_text(screen, f"Score: {score}", SCORE_COLOR, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50), align="center")
        self.render_text(screen, f"High Score: {high_score}", SCORE_COLOR, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), align="center")

        # Restart text
        self.render_text(screen, "Press ENTER to Restart", SCORE_COLOR, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100), align="center")

    def render_game(self, screen, snake, food, obstacles, score, high_score, start_time, screenshot_manager=None):
        """Render the game screen with all components."""
        # Draw background with grid
        screen.blit(self.background, (0, 0))

        # Game objects
        snake.render(screen)
        food.render(screen)
        obstacles.render(screen)

        # Draw scores
        self.render_text(screen, f"Score: {score}", SCORE_COLOR, (10, 10), 32, align="left")
        self.render_text(screen, f"High Score: {high_score}", SCORE_COLOR, (WINDOW_WIDTH - 10, 10), 32, align="right")

        # Calculate and render timer
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        self.render_text(screen, f"Time: {elapsed_time}s", SCORE_COLOR, (WINDOW_WIDTH // 2, 20), 32, align="center")

        if screenshot_manager:
            screenshot_manager.update(screen)

    def show_pause_menu(self, screen, score):
        """Show pause menu screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        # Pause title
        self.render_text(screen, "PAUSED", GAME_OVER_COLOR, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50), 64, align="center")

        # Score
        self.render_text(screen, f"Current Score: {score}", SCORE_COLOR, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20), align="center")

        # Controls
        self.render_text(screen, "Press ESC to Resume", SCORE_COLOR, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80), align="center")

        # Quit
        self.render_text(screen, "Press Q to Quit", SCORE_COLOR, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 110), align="center")

        pygame.display.flip()

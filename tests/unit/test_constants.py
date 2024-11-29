import unittest
import pygame
from src.constants import draw_rounded_rect, draw_grid


class TestConstants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.Surface((800, 600))

    def test_draw_rounded_rect(self):
        """Test drawing rounded rectangle"""
        surface = pygame.Surface((100, 100))
        color = (255, 0, 0)
        rect = pygame.Rect(10, 10, 80, 80)
        draw_rounded_rect(surface, color, rect, 10)
        # Check if the surface was modified (not black)
        self.assertNotEqual(surface.get_at((50, 50)), (0, 0, 0, 255))

    def test_draw_grid(self):
        """Test drawing grid lines"""
        surface = pygame.Surface((800, 600))
        initial_color = surface.get_at((0, 0))
        draw_grid(surface)
        # Check if grid lines were drawn (color changed)
        self.assertNotEqual(surface.get_at((40, 0)), initial_color)
        self.assertNotEqual(surface.get_at((0, 40)), initial_color)

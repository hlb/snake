import math
import random
from dataclasses import dataclass
import pygame


@dataclass
class ParticleVisuals:
    """Visual properties of a particle."""

    color: tuple[int, int, int]
    alpha: int = 255
    size: int = 0

    def __post_init__(self):
        if self.size == 0:
            self.size = random.randint(3, 6)


class Particle:
    def __init__(self, x, y, color, velocity, lifetime=1.0):
        # Essential attributes for physics/movement
        self.x = x
        self.y = y
        self.velocity = velocity
        self.lifetime = lifetime
        self.birth_time = pygame.time.get_ticks()

        # Visual properties grouped in dataclass
        self.visuals = ParticleVisuals(color=color)

    def update(self):
        current_time = pygame.time.get_ticks()
        age = (current_time - self.birth_time) / 1000.0  # Convert to seconds
        if age > self.lifetime:
            return False

        # Update position with gravity effect
        self.velocity = (
            self.velocity[0] * 0.98,  # Horizontal drag
            self.velocity[1] + 0.1,  # Gravity
        )
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # Fade out
        self.visuals.alpha = int(255 * (1 - age / self.lifetime))
        return True

    def render(self, screen):
        if self.visuals.alpha <= 0:
            return

        surface = pygame.Surface((self.visuals.size * 2, self.visuals.size * 2), pygame.SRCALPHA)
        color_with_alpha = (*self.visuals.color, self.visuals.alpha)
        pygame.draw.circle(surface, color_with_alpha, (self.visuals.size, self.visuals.size), self.visuals.size)
        screen.blit(surface, (int(self.x - self.visuals.size), int(self.y - self.visuals.size)))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=10):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)  # Increased speed range
            velocity = (
                math.cos(angle) * speed,
                math.sin(angle) * speed - 2,
            )  # Initial upward velocity
            lifetime = random.uniform(0.8, 1.2)  # Slightly longer lifetime
            self.particles.append(Particle(x, y, color, velocity, lifetime))

    def update(self):
        self.particles = [p for p in self.particles if p.update()]

    def render(self, screen):
        for particle in self.particles:
            particle.render(screen)

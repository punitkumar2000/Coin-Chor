"""Simple world objects. Later days add blocks, power-ups and moving platforms."""

import pygame

from settings import COIN_COLOR, DIRT, GRASS


class Platform:
    def __init__(self, x, y, width, height=24):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, DIRT, self.rect)
        pygame.draw.rect(surface, GRASS, (self.rect.x, self.rect.y, self.rect.width, 7))


class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 18, 18)
        self.collected = False

    def draw(self, surface):
        if not self.collected:
            pygame.draw.circle(surface, COIN_COLOR, self.rect.center, 9)

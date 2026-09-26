"""A basic walking enemy. Enemy types and a manager arrive in later phases."""

import pygame

from settings import ENEMY_COLOR


class Enemy:
    def __init__(self, x, y, left_bound, right_bound):
        self.rect = pygame.Rect(x, y, 32, 30)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = 2

    def update(self):
        self.rect.x += self.speed
        if self.rect.left <= self.left_bound or self.rect.right >= self.right_bound:
            self.speed *= -1

    def draw(self, surface):
        pygame.draw.ellipse(surface, ENEMY_COLOR, self.rect)

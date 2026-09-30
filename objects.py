"""Simple world objects. Later days add blocks, power-ups and moving platforms."""

import pygame

from settings import COIN_COLOR, DIRT, GRASS


class Platform:
    def __init__(self, x, y, width, height=24):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, DIRT, self.rect)

        # Small marks on the dirt
        for x in range(self.rect.left + 8, self.rect.right - 4, 28):
            y = self.rect.top + 16 + ((x // 28) % 2) * 7
            pygame.draw.circle(surface, (115, 75, 48), (x, y), 2)

        # Grass strip and blades
        pygame.draw.rect(
            surface, GRASS,
            (self.rect.x, self.rect.y, self.rect.width, 7),
        )
        for x in range(self.rect.left + 5, self.rect.right - 3, 18):
            pygame.draw.line(
                surface, (80, 190, 90),
                (x, self.rect.y + 6), (x + 2, self.rect.y + 1), 2,
            )


class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 18, 18)
        self.collected = False

    def draw(self, surface):
        if not self.collected:
            pulse = (pygame.time.get_ticks() // 180) % 2
            radius = 8 + pulse

            pygame.draw.circle(surface, COIN_COLOR, self.rect.center, radius)
            pygame.draw.circle(
                surface,
                (255, 245, 170),
                (self.rect.centerx - 2, self.rect.centery - 3),
                3,
            )
class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 24)
        self.collected = False

    def draw(self, surface):
        if not self.collected:
            pygame.draw.circle(surface, (250, 210, 55), self.rect.center, 12)
            pygame.draw.polygon(
                surface,
                (85, 65, 35),
                [
                    (self.rect.x + 14, self.rect.y + 2),
                    (self.rect.x + 8, self.rect.y + 13),
                    (self.rect.x + 13, self.rect.y + 13),
                    (self.rect.x + 10, self.rect.y + 22),
                    (self.rect.x + 18, self.rect.y + 10),
                    (self.rect.x + 13, self.rect.y + 10),
                ],
            )
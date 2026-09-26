"""The player character and its first-day movement."""

import pygame

from settings import GRAVITY, JUMP_SPEED, PLAYER_COLOR, PLAYER_SPEED, SCREEN_HEIGHT


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 34, 46)
        self.velocity_y = 0
        self.on_ground = False

    def update(self, keys, platforms):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.velocity_y = JUMP_SPEED
            self.on_ground = False

        self.velocity_y += GRAVITY
        self.rect.y += int(self.velocity_y)
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(1600, self.rect.right)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.topleft = (60, 400)
            self.velocity_y = 0

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect, border_radius=6)

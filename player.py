"""The player character, movement, jumping, and platform collisions."""

import pygame

from settings import (
    GRAVITY,
    JUMP_SPEED,
    PLAYER_COLOR,
    PLAYER_SPEED,
    SCREEN_HEIGHT,
)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 34, 46)
        self.velocity_y = 0
        self.on_ground = False

    def update(self, keys, platforms):
        # Save the old position so we can tell which side hit a platform.
        previous_rect = self.rect.copy()

        # Move left or right.
        move_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x += PLAYER_SPEED

        self.rect.x += move_x

        # Stop the player at the sides of platforms.
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if move_x > 0:
                    self.rect.right = platform.rect.left
                elif move_x < 0:
                    self.rect.left = platform.rect.right

        # Keep the player inside the level.
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(1600, self.rect.right)

        # Jump only when standing on a platform.
        jump_pressed = (
            keys[pygame.K_SPACE]
            or keys[pygame.K_UP]
            or keys[pygame.K_w]
        )
        if jump_pressed and self.on_ground:
            self.velocity_y = JUMP_SPEED
            self.on_ground = False

        # Apply gravity and move vertically.
        self.velocity_y += GRAVITY
        move_y = int(self.velocity_y)
        self.rect.y += move_y
        self.on_ground = False

        # Land on platforms, or bump the underside when jumping.
        for platform in platforms:
            if not self.rect.colliderect(platform.rect):
                continue

            if move_y >= 0 and previous_rect.bottom <= platform.rect.top:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True
            elif move_y < 0 and previous_rect.top >= platform.rect.bottom:
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0

        # If the player falls off the level, return them to the start.
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.topleft = (60, 400)
            self.velocity_y = 0
            self.on_ground = False

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect, border_radius=6)
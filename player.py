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
        self.speed_boost_timer = 0
        self.is_moving = False

    def update(self, keys, platforms):
        # Save the old position so we can tell which side hit a platform.
        previous_rect = self.rect.copy()

        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1

        move_speed = PLAYER_SPEED * 2 if self.speed_boost_timer > 0 else PLAYER_SPEED
        # Move left or right.
        move_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x -= move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x += move_speed

        self.rect.x += move_x

        # Stop the player at the sides of platforms.
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if move_x > 0:
                    self.rect.right = platform.rect.left
                elif move_x < 0:
                    self.rect.left = platform.rect.right
        self.is_moving = move_x != 0 and self.rect.x != previous_rect.x
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
        x = self.rect.x
        y = self.rect.y

        # Tail
        pygame.draw.lines(
            surface, (145, 115, 95), False,
            [(x + 9, y + 33), (x + 2, y + 37), (x + 1, y + 32)],
            3,
        )

        # Body and animated feet
        pygame.draw.ellipse(surface, (155, 145, 130), (x + 7, y + 20, 23, 20))
        pygame.draw.ellipse(surface, (205, 190, 170), (x + 12, y + 25, 15, 11))

        moving = getattr(self, "is_moving", False)
        if moving:
            step = (pygame.time.get_ticks() // 120) % 2
            left_foot_y = y + 38 + (step * 2)
            right_foot_y = y + 38 + ((1 - step) * 2)
        else:
            left_foot_y = right_foot_y = y + 38

        pygame.draw.ellipse(surface, (90, 80, 75), (x + 6, left_foot_y, 11, 7))
        pygame.draw.ellipse(surface, (90, 80, 75), (x + 19, right_foot_y, 11, 7))

        # Head and ears
        pygame.draw.circle(surface, (155, 145, 130), (x + 12, y + 10), 7)
        pygame.draw.circle(surface, (155, 145, 130), (x + 24, y + 10), 7)
        pygame.draw.circle(surface, (215, 155, 155), (x + 12, y + 10), 4)
        pygame.draw.circle(surface, (215, 155, 155), (x + 24, y + 10), 4)
        pygame.draw.ellipse(surface, (175, 165, 150), (x + 7, y + 6, 23, 20))

        # Face
        pygame.draw.ellipse(surface, (225, 210, 190), (x + 10, y + 14, 18, 10))
        pygame.draw.circle(surface, (35, 45, 60), (x + 15, y + 13), 2)
        pygame.draw.circle(surface, (35, 45, 60), (x + 23, y + 13), 2)
        pygame.draw.circle(surface, (205, 110, 125), (x + 19, y + 18), 2)

        # Whiskers
        pygame.draw.line(surface, (75, 70, 65), (x + 13, y + 19), (x + 2, y + 17), 1)
        pygame.draw.line(surface, (75, 70, 65), (x + 13, y + 21), (x + 2, y + 23), 1)
        pygame.draw.line(surface, (75, 70, 65), (x + 25, y + 19), (x + 33, y + 17), 1)
        pygame.draw.line(surface, (75, 70, 65), (x + 25, y + 21), (x + 33, y + 23), 1)
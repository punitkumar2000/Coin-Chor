"""Walking, jumping enemy and its simple shape-drawn projectiles."""

import pygame

from settings import ENEMY_COLOR


class Bullet:
    """A small projectile fired horizontally toward the player's current side."""

    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 12, 6)
        self.direction = direction
        self.speed = 7

    def update(self):
        self.rect.x += self.speed * self.direction

    def draw(self, surface):
        pygame.draw.rect(surface, (230, 65, 55), self.rect, border_radius=3)


class Enemy:
    """Patrols between two points, jumps now and then, and fires at the player."""

    def __init__(self, x, y, left_bound, right_bound):
        self.rect = pygame.Rect(x, y, 34, 30)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = 2
        self.direction = 1

        self.ground_y = y
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_speed = -10
        self.jump_timer = 0
        self.jump_delay = 120

        self.shoot_timer = 0
        self.shoot_delay = 90

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= self.right_bound:
            self.rect.right = self.right_bound
            self.direction = -1
        elif self.rect.left <= self.left_bound:
            self.rect.left = self.left_bound
            self.direction = 1

        self.jump_timer += 1
        if self.jump_timer >= self.jump_delay and self.rect.y >= self.ground_y:
            self.velocity_y = self.jump_speed
            self.jump_timer = 0

        self.velocity_y += self.gravity
        self.rect.y += int(self.velocity_y)
        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.velocity_y = 0

        self.shoot_timer += 1

    def ready_to_shoot(self):
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            return True
        return False

    def shoot(self, player_rect):
        direction = -1 if player_rect.centerx < self.rect.centerx else 1
        bullet_x = self.rect.left if direction == -1 else self.rect.right
        return Bullet(bullet_x, self.rect.centery, direction)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)

    def draw(self, surface):
        x = self.rect.x
        y = self.rect.y

        # Tail
        pygame.draw.lines(
            surface, (205, 125, 65), False,
            [(x + 5, y + 20), (x - 2, y + 24), (x - 4, y + 19)],
            3,
        )

        # Body and animated paws
        pygame.draw.ellipse(surface, (220, 135, 65), (x + 5, y + 12, 24, 16))
        pygame.draw.ellipse(surface, (245, 190, 125), (x + 11, y + 17, 13, 9))

        step = (pygame.time.get_ticks() // 140) % 2
        left_paw_y = y + 25 + (step * 2)
        right_paw_y = y + 25 + ((1 - step) * 2)

        pygame.draw.ellipse(surface, (90, 65, 50), (x + 7, left_paw_y, 10, 5))
        pygame.draw.ellipse(surface, (90, 65, 50), (x + 21, right_paw_y, 10, 5))

        # Head and pointed ears
        pygame.draw.polygon(surface, (220, 135, 65), [(x + 8, y + 12), (x + 7, y + 1), (x + 17, y + 8)])
        pygame.draw.polygon(surface, (220, 135, 65), [(x + 18, y + 8), (x + 29, y + 1), (x + 27, y + 14)])
        pygame.draw.ellipse(surface, (230, 150, 80), (x + 7, y + 6, 22, 19))
        pygame.draw.polygon(surface, (235, 145, 150), [(x + 9, y + 6), (x + 9, y + 3), (x + 14, y + 7)])
        pygame.draw.polygon(surface, (235, 145, 150), [(x + 21, y + 7), (x + 27, y + 3), (x + 26, y + 8)])

        # Face
        pygame.draw.ellipse(surface, (250, 220, 185), (x + 12, y + 15, 13, 7))
        pygame.draw.circle(surface, (35, 45, 60), (x + 14, y + 13), 2)
        pygame.draw.circle(surface, (35, 45, 60), (x + 23, y + 13), 2)
        pygame.draw.circle(surface, (190, 80, 95), (x + 19, y + 18), 2)
        pygame.draw.line(surface, (80, 65, 55), (x + 19, y + 19), (x + 19, y + 22), 1)
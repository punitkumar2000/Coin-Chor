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
        pygame.draw.ellipse(surface, ENEMY_COLOR, self.rect)
        eye_x = self.rect.centerx + (7 * self.direction)
        pygame.draw.circle(surface, (255, 255, 255), (eye_x, self.rect.y + 10), 4)
        pygame.draw.circle(surface, (35, 45, 60), (eye_x + self.direction, self.rect.y + 10), 2)
        gun_x = self.rect.right if self.direction == 1 else self.rect.left - 10
        pygame.draw.rect(surface, (80, 80, 80), (gun_x, self.rect.centery - 3, 10, 6))

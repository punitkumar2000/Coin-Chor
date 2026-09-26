"""Game loop and integration for the player, stages, enemies, and projectiles."""

import pygame

from levels import build_stage_one
from player import Player
from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, SKY, WINDOW_TITLE
from ui import UI


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.running = True
        self.started = False
        self.camera_x = 0
        self.reset_stage()

    def reset_stage(self):
        self.stage = build_stage_one()
        self.player = Player(60, 400)
        self.bullets = []
        self.player_lives = 3
        self.hit_cooldown = 0
        self.game_over = False
        self.camera_x = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.started = True
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_stage()
                    self.started = True

    def lose_life(self):
        if self.hit_cooldown > 0 or self.game_over:
            return
        self.player_lives -= 1
        self.hit_cooldown = 75
        self.player.rect.topleft = (60, 400)
        self.player.velocity_y = 0
        if self.player_lives <= 0:
            self.game_over = True

    def update(self):
        if not self.started or self.game_over:
            return

        keys = pygame.key.get_pressed()
        self.player.update(keys, self.stage["platforms"])

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        for enemy in self.stage["enemies"]:
            enemy.update()
            if enemy.ready_to_shoot():
                self.bullets.append(enemy.shoot(self.player.rect))
            if enemy.check_collision(self.player.rect) and self.hit_cooldown == 0:
                self.lose_life()

        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.colliderect(self.player.rect):
                self.lose_life()
                bullet.rect.x = -100

        self.bullets = [
            bullet for bullet in self.bullets
            if bullet.rect.right > 0 and bullet.rect.left < 1600
        ]

        for coin in self.stage["coins"]:
            if not coin.collected and self.player.rect.colliderect(coin.rect):
                coin.collected = True

        self.camera_x = max(
            0,
            min(self.player.rect.centerx - SCREEN_WIDTH // 2, 1600 - SCREEN_WIDTH),
        )

    def draw(self):
        self.screen.fill(SKY)
        if not self.started:
            self.ui.draw_start(self.screen)
        elif self.game_over:
            self.ui.draw_game_over(self.screen)
        else:
            world = pygame.Surface((1600, SCREEN_HEIGHT))
            world.fill(SKY)
            for platform in self.stage["platforms"]:
                platform.draw(world)
            for coin in self.stage["coins"]:
                coin.draw(world)
            for enemy in self.stage["enemies"]:
                enemy.draw(world)
            for bullet in self.bullets:
                bullet.draw(world)
            self.player.draw(world)
            self.screen.blit(world, (-self.camera_x, 0))
            coin_count = sum(1 for coin in self.stage["coins"] if coin.collected)
            self.ui.draw_hud(
                self.screen, self.stage["info"]["name"], coin_count, self.player_lives
            )
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

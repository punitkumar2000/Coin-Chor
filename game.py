"""Game loop and first-day integration of the game modules."""

import pygame

from levels import build_stage_one
from player import Player
from settings import DARK, FPS, SCREEN_HEIGHT, SCREEN_WIDTH, SKY, WINDOW_TITLE
from ui import UI


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.stage = build_stage_one()
        self.player = Player(60, 400)
        self.running = True
        self.started = False
        self.camera_x = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.started = True

    def update(self):
        if not self.started:
            return
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.stage["platforms"])
        for enemy in self.stage["enemies"]:
            enemy.update()
        for coin in self.stage["coins"]:
            if not coin.collected and self.player.rect.colliderect(coin.rect):
                coin.collected = True
        self.camera_x = max(0, min(self.player.rect.centerx - SCREEN_WIDTH // 2, 1600 - SCREEN_WIDTH))

    def draw(self):
        self.screen.fill(SKY)
        if not self.started:
            self.ui.draw_start(self.screen)
        else:
            world = pygame.Surface((1600, SCREEN_HEIGHT))
            world.fill(SKY)
            for platform in self.stage["platforms"]:
                platform.draw(world)
            for coin in self.stage["coins"]:
                coin.draw(world)
            for enemy in self.stage["enemies"]:
                enemy.draw(world)
            self.player.draw(world)
            self.screen.blit(world, (-self.camera_x, 0))
            count = sum(1 for coin in self.stage["coins"] if coin.collected)
            self.ui.draw_hud(self.screen, self.stage["info"]["name"], count)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

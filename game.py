"""Main game loop and integration for players, stages, enemies, and projectiles."""

import pygame

from levels import build_stage_one, build_stage_two, build_stage_three
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
        self.stage_number = 1
        self.stage = build_stage_one()
        self.player = Player(60, 400)
        self.bullets = []
        self.player_lives = 3
        self.hit_cooldown = 0
        self.game_over = False
        self.game_won = False
        self.camera_x = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.started = True
                elif event.key == pygame.K_r and (self.game_over or self.game_won):
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

    def check_stage_exit(self):
        all_coins_collected = all(coin.collected for coin in self.stage["coins"])
        reached_exit = self.player.rect.right >= 1540

        if not reached_exit:
            return

        if self.stage_number == 1:
            self.stage_number = 2
            self.stage = build_stage_two()
        elif self.stage_number == 2:
            self.stage_number = 3
            self.stage = build_stage_three()
        else:
            self.game_won = True
            return

        self.player = Player(60, 400)
        self.bullets.clear()
        self.camera_x = 0

    def update(self):
        if not self.started or self.game_over or self.game_won:
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
        for powerup in self.stage.get("powerups", []):
            if not powerup.collected and self.player.rect.colliderect(powerup.rect):
                powerup.collected = True
                self.player.speed_boost_timer = 300

        self.check_stage_exit()

        self.camera_x = max(
            0,
            min(self.player.rect.centerx - SCREEN_WIDTH // 2, 1600 - SCREEN_WIDTH),
        )

    def draw_exit_gate(self, world):
        pygame.draw.rect(world, (90, 70, 55), (1530, 405, 8, 85))
        pygame.draw.polygon(
            world,
            (245, 190, 65),
            [(1538, 405), (1580, 420), (1538, 438)],
        )


    def draw_scenery(self, world):
        if self.stage_number == 1:
            # Green Meadow hills
            pygame.draw.ellipse(world, (125, 190, 120), (-100, 365, 650, 260))
            pygame.draw.ellipse(world, (105, 175, 105), (400, 390, 750, 250))
            pygame.draw.ellipse(world, (85, 155, 95), (950, 360, 750, 280))

            # Clouds
            for x, y in [(120, 115), (410, 175), (760, 95), (1190, 145), (1450, 80)]:
                pygame.draw.ellipse(world, (240, 250, 255), (x, y + 8, 55, 22))
                pygame.draw.circle(world, (240, 250, 255), (x + 18, y + 8), 16)
                pygame.draw.circle(world, (240, 250, 255), (x + 38, y + 5), 20)

        elif self.stage_number == 2:
            # Moonlit Cave stars
            stars = [(100, 80), (260, 145), (430, 65), (620, 125),
                     (810, 75), (990, 150), (1190, 90), (1400, 135), (1530, 60)]
            for x, y in stars:
                pygame.draw.circle(world, (225, 225, 255), (x, y), 3)

            # Hanging cave rocks
            for x, width, height in [(80, 100, 75), (340, 130, 95),
                                     (700, 110, 65), (1050, 140, 100),
                                     (1390, 120, 80)]:
                pygame.draw.polygon(
                    world,
                    (70, 58, 95),
                    [(x, 0), (x + width, 0), (x + width // 2, height)],
                )

        else:
            # Sunset Castle in the distance
            pygame.draw.ellipse(world, (135, 83, 110), (-80, 405, 700, 180))
            pygame.draw.ellipse(world, (120, 70, 100), (700, 390, 950, 200))

            # Castle walls and towers
            pygame.draw.rect(world, (75, 53, 88), (260, 300, 280, 190))
            pygame.draw.rect(world, (65, 46, 80), (300, 250, 65, 240))
            pygame.draw.rect(world, (65, 46, 80), (435, 250, 65, 240))

            # Tower roofs
            pygame.draw.polygon(world, (55, 42, 72), [(285, 250), (380, 250), (332, 195)])
            pygame.draw.polygon(world, (55, 42, 72), [(420, 250), (515, 250), (468, 195)])

            # Glowing windows
            pygame.draw.rect(world, (245, 190, 100), (325, 330, 28, 45))
            pygame.draw.rect(world, (245, 190, 100), (445, 330, 28, 45))
            pygame.draw.rect(world, (245, 190, 100), (380, 400, 40, 90))
     
    def draw(self):
        self.screen.fill(SKY)

        if not self.started:
            self.ui.draw_start(self.screen)
        elif self.game_over:
            self.ui.draw_game_over(self.screen)
        elif self.game_won:
            self.ui.draw_win(self.screen)
        else:
            world = pygame.Surface((1600, SCREEN_HEIGHT))
            world.fill(self.stage["info"]["background"])
            self.draw_scenery(world)

            for platform in self.stage["platforms"]:
                platform.draw(world)

            for coin in self.stage["coins"]:
                coin.draw(world)

            for powerup in self.stage.get("powerups", []):
                powerup.draw(world)

            for enemy in self.stage["enemies"]:
                enemy.draw(world)

            for bullet in self.bullets:
                bullet.draw(world)

            self.draw_exit_gate(world)
            self.player.draw(world)
            self.screen.blit(world, (-self.camera_x, 0))

            coin_count = sum(1 for coin in self.stage["coins"] if coin.collected)
            self.ui.draw_hud(
                self.screen,
                self.stage["info"]["name"],
                coin_count,
                self.player_lives,
                self.player.speed_boost_timer,
            )

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
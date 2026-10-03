"""Main game loop and integration for players, stages, enemies, and projectiles."""

import pygame

from levels import build_stage_one, build_stage_two, build_stage_three
from player import Player
from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, SKY, WINDOW_TITLE
from ui import UI
from sound_effects import SoundEffects


class Game:
    def __init__(self):
        pygame.init()
        self.sounds = SoundEffects()
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
        self.respawn_position = (60, 400)
        self.bullets = []
        self.stomp_effect_timer = 0
        self.stomp_effect_pos = (0, 0)
        self.player_lives = 3
        self.hit_cooldown = 0
        self.game_over = False
        self.game_won = False
        self.paused = False
        self.exit_locked = False
        self.camera_x = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.started = True
                elif (
                    event.key == pygame.K_p
                    and self.started
                    and not self.game_over
                    and not self.game_won
                ):
                    self.paused = not self.paused
                elif event.key == pygame.K_r and (
                    self.game_over or self.game_won
                ):
                    self.reset_stage()
                    self.started = True

    def lose_life(self):
        if self.hit_cooldown > 0 or self.game_over:
            return

        self.player_lives -= 1
        self.sounds.play_damage()
        self.hit_cooldown = 75
        self.player.rect.topleft = self.respawn_position
        self.player.velocity_y = 0

        if self.player_lives <= 0:
            self.game_over = True

    def check_stage_exit(self):
        all_coins_collected = all(
            coin.collected for coin in self.stage["coins"]
        )
        boss_alive = any(
            getattr(enemy, "is_boss", False)
            for enemy in self.stage["enemies"]
        )
        reached_exit = self.player.rect.right >= 1540

        self.exit_locked = reached_exit and (
            not all_coins_collected or boss_alive
        )

        if not reached_exit or not all_coins_collected or boss_alive:
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
        self.respawn_position = (60, 400)
        self.bullets.clear()
        self.stomp_effect_timer = 0
        self.exit_locked = False
        self.camera_x = 0

    def update(self):
        if (
            not self.started
            or self.game_over
            or self.game_won
            or self.paused
        ):
            return

        if self.stomp_effect_timer > 0:
            self.stomp_effect_timer -= 1

        keys = pygame.key.get_pressed()
        jump_pressed = (
            keys[pygame.K_SPACE]
            or keys[pygame.K_UP]
            or keys[pygame.K_w]
        )

        if jump_pressed and self.player.on_ground:
            self.sounds.play_jump()

        self.player.update(keys, self.stage["platforms"])

        # X=800 cross karne par checkpoint activate hota hai.
        if self.player.rect.centerx >= 800:
            self.respawn_position = (760, 450)

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        for enemy in self.stage["enemies"][:]:
            enemy.update()

            if enemy.ready_to_shoot():
                self.bullets.append(enemy.shoot(self.player.rect))

            if enemy.check_collision(self.player.rect) and self.hit_cooldown == 0:
                # Neeche girte hue enemy ke upar land kiya toh stomp hoga
                if (
                    self.player.velocity_y > 0
                    and self.player.rect.bottom < enemy.rect.centery
                ):
                    self.stomp_effect_pos = enemy.rect.center
                    self.stomp_effect_timer = 18
                    self.sounds.play_stomp()
                    self.player.velocity_y = -10
                    self.hit_cooldown = 18

                    if getattr(enemy, "is_boss", False):
                        enemy.health -= 1
                        if enemy.health <= 0:
                            self.stage["enemies"].remove(enemy)
                    else:
                        self.stage["enemies"].remove(enemy)
                else:
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
                self.sounds.play_coin()

        for powerup in self.stage.get("powerups", []):
            if not powerup.collected and self.player.rect.colliderect(powerup.rect):
                powerup.collected = True
                self.player.speed_boost_timer = 300

        self.check_stage_exit()

        self.camera_x = max(
            0,
            min(
                self.player.rect.centerx - SCREEN_WIDTH // 2,
                1600 - SCREEN_WIDTH,
            ),
        )

    def draw_exit_gate(self, world):
        # Gate pole and base
        pygame.draw.rect(world, (90, 70, 55), (1530, 405, 8, 85))
        pygame.draw.rect(world, (145, 115, 80), (1527, 480, 14, 10))
        pygame.draw.circle(world, (255, 220, 120), (1534, 402), 5)

        # Gently waving flag
        wave = (pygame.time.get_ticks() // 250) % 2
        tip_x = 1580 if wave == 0 else 1573
        middle_y = 421 if wave == 0 else 424

        pygame.draw.polygon(
            world,
            (245, 190, 65),
            [(1538, 405), (tip_x, middle_y), (1538, 438)],
        )
        pygame.draw.line(
            world,
            (255, 230, 145),
            (1541, 411),
            (tip_x - 8, middle_y),
            2,
        )

    def draw_scenery(self, world):
        if self.stage_number == 1:
            # Green Meadow hills
            pygame.draw.ellipse(world, (125, 190, 120), (-100, 365, 650, 260))
            pygame.draw.ellipse(world, (105, 175, 105), (400, 390, 750, 250))
            pygame.draw.ellipse(world, (85, 155, 95), (950, 360, 750, 280))

            # Clouds
            for x, y in [
                (120, 115),
                (410, 175),
                (760, 95),
                (1190, 145),
                (1450, 80),
            ]:
                pygame.draw.ellipse(
                    world, (240, 250, 255), (x, y + 8, 55, 22)
                )
                pygame.draw.circle(
                    world, (240, 250, 255), (x + 18, y + 8), 16
                )
                pygame.draw.circle(
                    world, (240, 250, 255), (x + 38, y + 5), 20
                )

            # Small flowers in the meadow
            for x, y, color in [
                (70, 460, (255, 220, 90)),
                (385, 465, (250, 130, 160)),
                (610, 450, (255, 220, 90)),
                (920, 465, (250, 130, 160)),
                (1170, 455, (255, 220, 90)),
                (1510, 465, (250, 130, 160)),
            ]:
                pygame.draw.line(
                    world, (45, 125, 65), (x, y), (x, y + 14), 2
                )
                pygame.draw.circle(world, color, (x, y), 4)
                pygame.draw.circle(
                    world, (255, 245, 220), (x - 4, y), 3
                )
                pygame.draw.circle(
                    world, (255, 245, 220), (x + 4, y), 3
                )

        elif self.stage_number == 2:
            # Moonlit Cave stars
            stars = [
                (100, 80),
                (260, 145),
                (430, 65),
                (620, 125),
                (810, 75),
                (990, 150),
                (1190, 90),
                (1400, 135),
                (1530, 60),
            ]
            for x, y in stars:
                pygame.draw.circle(world, (225, 225, 255), (x, y), 3)

            # Hanging cave rocks
            for x, width, height in [
                (80, 100, 75),
                (340, 130, 95),
                (700, 110, 65),
                (1050, 140, 100),
                (1390, 120, 80),
            ]:
                pygame.draw.polygon(
                    world,
                    (70, 58, 95),
                    [
                        (x, 0),
                        (x + width, 0),
                        (x + width // 2, height),
                    ],
                )

            # Glowing cave crystals
            for x, y, color in [
                (180, 455, (90, 235, 245)),
                (560, 450, (175, 125, 255)),
                (900, 460, (90, 235, 245)),
                (1280, 450, (175, 125, 255)),
            ]:
                pygame.draw.polygon(
                    world,
                    color,
                    [
                        (x, y + 22),
                        (x - 10, y),
                        (x - 4, y + 3),
                        (x, y - 14),
                        (x + 5, y + 2),
                        (x + 11, y + 22),
                    ],
                )
                pygame.draw.line(
                    world, (235, 250, 255), (x, y - 8), (x - 3, y + 10), 2
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
            pygame.draw.polygon(
                world, (55, 42, 72), [(285, 250), (380, 250), (332, 195)]
            )
            pygame.draw.polygon(
                world, (55, 42, 72), [(420, 250), (515, 250), (468, 195)]
            )

            # Glowing windows
            pygame.draw.rect(world, (245, 190, 100), (325, 330, 28, 45))
            pygame.draw.rect(world, (245, 190, 100), (445, 330, 28, 45))
            pygame.draw.rect(world, (245, 190, 100), (380, 400, 40, 90))

            # Setting sun and castle flags
            pygame.draw.circle(world, (255, 175, 105), (1350, 190), 58)
            pygame.draw.circle(world, (255, 205, 125), (1350, 190), 43)

            pygame.draw.line(
                world, (225, 205, 175), (332, 178), (332, 205), 3
            )
            pygame.draw.polygon(
                world,
                (235, 95, 110),
                [(334, 180), (365, 188), (334, 197)],
            )

            pygame.draw.line(
                world, (225, 205, 175), (468, 178), (468, 205), 3
            )
            pygame.draw.polygon(
                world,
                (100, 190, 220),
                [(470, 180), (500, 188), (470, 197)],
            )

    def draw(self):
        self.screen.fill(SKY)

        if not self.started:
            self.ui.draw_start(self.screen)
        elif self.game_over:
            self.ui.draw_game_over(self.screen)
        elif self.game_won:
            self.ui.draw_win(self.screen)
        elif self.paused:
            self.ui.draw_pause(self.screen)
        else:
            world = pygame.Surface((1600, SCREEN_HEIGHT))
            world.fill(self.stage["info"]["background"])
            self.draw_scenery(world)

            for platform in self.stage["platforms"]:
                platform.draw(world)

            # Gray checkpoint becomes green after activation.
            flag_color = (
                (65, 210, 130)
                if self.respawn_position != (60, 400)
                else (185, 185, 195)
            )

            pygame.draw.rect(world, (90, 70, 55), (796, 350, 6, 55))
            pygame.draw.polygon(
                world,
                flag_color,
                [(802, 351), (836, 361), (802, 373)],
            )
            pygame.draw.circle(world, (255, 245, 190), (799, 348), 4)

            for coin in self.stage["coins"]:
                coin.draw(world)

            for powerup in self.stage.get("powerups", []):
                powerup.draw(world)

            for enemy in self.stage["enemies"]:
                enemy.draw(world)

            if self.stomp_effect_timer > 0:
                effect_age = 18 - self.stomp_effect_timer
                radius = 8 + effect_age * 2
                pygame.draw.circle(
                    world,
                    (255, 230, 120),
                    self.stomp_effect_pos,
                    radius,
                    3,
                )

            for bullet in self.bullets:
                bullet.draw(world)

            self.draw_exit_gate(world)
            self.player.draw(world)
            self.screen.blit(world, (-self.camera_x, 0))

            coin_count = sum(
                1 for coin in self.stage["coins"] if coin.collected
            )
            self.ui.draw_hud(
                self.screen,
                self.stage["info"]["name"],
                coin_count,
                self.player_lives,
                self.player.speed_boost_timer,
            )

            # Exit par coins baaki hon toh player ko reason dikhega.
            if self.exit_locked:
                boss_alive = any(
                    getattr(enemy, "is_boss", False)
                    for enemy in self.stage["enemies"]
                )
                coins_missing = coin_count < len(self.stage["coins"])

                if boss_alive and coins_missing:
                    message_text = "Collect all coins and defeat the boss!"
                elif boss_alive:
                    message_text = "Defeat the boss to unlock the exit!"
                else:
                    message_text = "Collect all coins to unlock the exit!"

                message = self.ui.font.render(
                    message_text,
                    True,
                    (255, 255, 255),
                )
                message_rect = message.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 42)
                )
                self.screen.blit(message, message_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
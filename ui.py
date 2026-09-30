"""Start screen, game HUD, and game-over screen."""

import pygame

from settings import DARK, WHITE


class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 30)
        self.title_font = pygame.font.Font(None, 58)

    def draw_hud(self, surface, stage_name, coin_count, lives, boost_timer=0):
        panel = pygame.Surface(
            (surface.get_width() - 24, 76),
            pygame.SRCALPHA,
        )
        pygame.draw.rect(
            panel,
            (255, 255, 255, 185),
            panel.get_rect(),
            border_radius=12,
        )
        surface.blit(panel, (12, 8))
        text = self.font.render(
            f"{stage_name}     Coins: {coin_count}     Lives: {lives}     "
            "Move: A/D or arrows | Jump: Space",
            True,
            DARK,
        )
        surface.blit(text, (18, 16))

        if boost_timer > 0:
            seconds_left = (boost_timer + 59) // 60
            boost_text = self.font.render(
                f"Speed boost: {seconds_left}s",
                True,
                DARK,
            )
            surface.blit(boost_text, (18, 50))

    def draw_start(self, surface):
        card = pygame.Surface((700, 250), pygame.SRCALPHA)
        pygame.draw.rect(
            card,
            (25, 45, 75, 190),
            card.get_rect(),
            border_radius=24,
        )
        pygame.draw.rect(
            card,
            (220, 240, 255, 180),
            card.get_rect(),
            width=2,
            border_radius=24,
        )
        surface.blit(
            card,
            (surface.get_width() // 2 - 350, 155),
        )
        title = self.title_font.render("JumpByte", True, WHITE)
        start_hint = self.font.render("Press ENTER to begin", True, WHITE)
        controls = self.font.render(
            "Move: A/D or arrows | Jump: Space | Pause: P",
            True,
            WHITE,
        )
        objective = self.font.render(
            "Reach the flag to move to the next world",
            True,
            WHITE,
        )

        surface.blit(title, title.get_rect(center=(surface.get_width() // 2, 210)))
        surface.blit(start_hint, start_hint.get_rect(center=(surface.get_width() // 2, 275)))
        surface.blit(controls, controls.get_rect(center=(surface.get_width() // 2, 325)))
        surface.blit(objective, objective.get_rect(center=(surface.get_width() // 2, 365)))

    def draw_game_over(self, surface):
        card = pygame.Surface((500, 190), pygame.SRCALPHA)
        pygame.draw.rect(
            card,
            (45, 25, 40, 205),
            card.get_rect(),
            border_radius=22,
        )
        pygame.draw.rect(
            card,
            (255, 210, 210, 180),
            card.get_rect(),
            width=2,
            border_radius=22,
        )
        surface.blit(
            card,
            (surface.get_width() // 2 - 250, 170),
        )
        title = self.title_font.render("Game Over", True, WHITE)
        hint = self.font.render("Press R to restart", True, WHITE)
        surface.blit(title, title.get_rect(center=(surface.get_width() // 2, 235)))
        surface.blit(hint, hint.get_rect(center=(surface.get_width() // 2, 290)))

    def draw_win(self, surface):
        card = pygame.Surface((700, 190), pygame.SRCALPHA)
        pygame.draw.rect(
            card,
            (30, 55, 45, 205),
            card.get_rect(),
            border_radius=22,
        )
        pygame.draw.rect(
            card,
            (220, 255, 220, 180),
            card.get_rect(),
            width=2,
            border_radius=22,
        )
        surface.blit(
            card,
            (surface.get_width() // 2 - 350, 170),
        )
        title = self.title_font.render("You Win!", True, WHITE)
        hint = self.font.render("You finished all three worlds! Press R to play again", True, WHITE)
        surface.blit(title, title.get_rect(center=(surface.get_width() // 2, 235)))
        surface.blit(hint, hint.get_rect(center=(surface.get_width() // 2, 290)))

    def draw_pause(self, surface):
        title = self.title_font.render("Paused", True, WHITE)
        hint = self.font.render("Press P to continue", True, WHITE)
        surface.blit(title, title.get_rect(center=(surface.get_width() // 2, 235)))
        surface.blit(hint, hint.get_rect(center=(surface.get_width() // 2, 290)))

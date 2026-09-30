"""Start screen, game HUD, and game-over screen."""

import pygame

from settings import DARK, WHITE


class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 30)
        self.title_font = pygame.font.Font(None, 58)

    def draw_hud(self, surface, stage_name, coin_count, lives, boost_timer=0):
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
        title = self.title_font.render("Game Over", True, WHITE)
        hint = self.font.render("Press R to restart", True, WHITE)
        surface.blit(title, title.get_rect(center=(surface.get_width() // 2, 235)))
        surface.blit(hint, hint.get_rect(center=(surface.get_width() // 2, 290)))

    def draw_win(self, surface):
        title = self.title_font.render("You Win!", True, WHITE)
        hint = self.font.render("You finished all three worlds! Press R to play again", True, WHITE)
        surface.blit(title, title.get_rect(center=(surface.get_width() // 2, 235)))
        surface.blit(hint, hint.get_rect(center=(surface.get_width() // 2, 290)))

    def draw_pause(self, surface):
        title = self.title_font.render("Paused", True, WHITE)
        hint = self.font.render("Press P to continue", True, WHITE)
        surface.blit(title, title.get_rect(center=(surface.get_width() // 2, 235)))
        surface.blit(hint, hint.get_rect(center=(surface.get_width() // 2, 290)))

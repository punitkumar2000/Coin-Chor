"""Start screen, game HUD, and game-over screen."""

import pygame

from settings import DARK, WHITE


class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 30)
        self.title_font = pygame.font.Font(None, 58)

    def draw_hud(self, surface, stage_name, coin_count, lives):
        text = self.font.render(
            f"{stage_name}     Coins: {coin_count}     Lives: {lives}     "
            "Move: A/D or arrows | Jump: Space",
            True,
            DARK,
        )
        surface.blit(text, (18, 16))

    def draw_start(self, surface):
        title = self.title_font.render("JumpByte", True, WHITE)
        hint = self.font.render("Press ENTER to begin", True, WHITE)
        surface.blit(title, title.get_rect(center=(surface.get_width() // 2, 220)))
        surface.blit(hint, hint.get_rect(center=(surface.get_width() // 2, 280)))

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

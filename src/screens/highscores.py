import asyncio
import pygame as pg
from highscore_handler import HighscoresHandler
from screens import BaseScreen, ScreenTypes
from constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app import App


class HighscoresScreen(BaseScreen):
    def __init__(self, app: "App"):
        self.app = app

    async def run(self) -> None:
        self.highscores = HighscoresHandler.get_highscores(self.app.config)

        font = self.app.small_font
        title_font = self.app.large_font
        line_height = font.get_linesize() + 8
        title_line_height = title_font.get_linesize() + 8
        title_surf = title_font.render("Highscores:", False, "yellow")

        x = SCREEN_WIDTH // 2

        running = True
        while running:
            self.app.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                        self.app.move_to(ScreenTypes.MAIN_MENU)

            self.app.screen.fill("black")
            y = 10
            self.app.screen.blit(title_surf, (x - title_surf.width // 2, y))
            y += title_line_height

            if not self.highscores:
                score_surf = font.render(
                    "No results have been recorded so far.", False, "yellow")
                self.app.screen.blit(score_surf,
                                     (x - score_surf.width // 2, y))
            else:
                for highscore in self.highscores:
                    name, score = list(highscore.items())[0]
                    score_str = name + ": " + str(score)
                    score_surf = font.render(score_str, False, "yellow")
                    self.app.screen.blit(score_surf,
                                         (x - score_surf.width // 2, y))
                    y += line_height

            hint_surf = font.render("ESC: back", True, "white")
            self.app.screen.blit(hint_surf, (x - hint_surf.width // 2,
                                             SCREEN_HEIGHT - line_height))

            pg.display.flip()

            await asyncio.sleep(0)

import asyncio
import pygame as pg
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app import App

from screens import BaseScreen, ScreenTypes
from highscore_handler import HighscoresHandler
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS


class GameEndScreen(BaseScreen):
    def __init__(self, app: "App", won: bool=False, score: int=0):
        self.app = app
        self.won = won
        self.score = score

        self.max_name_len = 10
        self.name_chars = []
        self.message = "YOU WON!" if won else "GAME OVER"
        self.msg_clr = "green" if won else "red"

        self.info_msg = "Type your name (A-Z, 0-9). Press ENTER to save"
        self.cursor_visible = True
        self.cursor_timer = 0

        self.running = True

    def save_and_exit(self) -> None:
        name = "".join(self.name_chars).strip()
        if not name:
            name = "Player"
        HighscoresHandler.store_highscores(self.app.config, name, self.score)
        self.running = False
        self.app.move_to(ScreenTypes.MAIN_MENU)

    def handle_text_input(self, event: pg.Event) -> None:
        if len(self.name_chars) >= self.max_name_len:
            return
        ch = event.unicode
        if not ch:
            return
        if ch.isalnum() or ch == " ":
            self.name_chars.append(ch)

    def handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.app.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    self.app.move_to(ScreenTypes.MAIN_MENU)
                elif event.key == pg.K_BACKSPACE:
                    if self.name_chars:
                        self.name_chars.pop()
                elif event.key == pg.K_RETURN:
                    self.save_and_exit()
                else:
                    self.handle_text_input(event)

    def get_name_field_text(self) -> str:
        undersc_len = self.max_name_len - len(self.name_chars)
        return "".join(self.name_chars) + "_" * undersc_len

    def update_cursor(self) -> None:
        self.cursor_timer += self.app.clock.get_time()
        if self.cursor_timer >= 450:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self) -> None:
        self.app.screen.fill("black")

        y = self.app.large_font.get_height()
        title_surf = self.app.large_font.render(self.message,
                                               False,
                                               self.msg_clr)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.app.screen.blit(title_surf, title_rect)

        y += self.app.large_font.get_height() * 2
        score_surf = self.app.small_font.render(f"SCORE: {self.score}", False, "yellow")
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.app.screen.blit(score_surf, score_rect)


        y += self.app.small_font.get_height() + self.app.large_font.get_height()
        name_field = ""
        if self.cursor_visible and len(self.name_chars) < self.max_name_len:
            name_field = "".join(self.name_chars) + "|" + "_" * (self.max_name_len - len(self.name_chars) - 1)
        else:
            name_field = "".join(self.name_chars) + "_" * (self.max_name_len - len(self.name_chars))
        name_surf = self.app.large_font.render(name_field, False, "yellow")
        name_rect = name_surf.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.app.screen.blit(name_surf, name_rect)

        y = SCREEN_HEIGHT - self.app.small_font.get_height() * 3
        prompt_surf = self.app.small_font.render(self.info_msg, False, "white")
        prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.app.screen.blit(prompt_surf, prompt_rect)

        y = SCREEN_HEIGHT - self.app.small_font.get_height()
        esc_surf = self.app.small_font.render("ESC: skip", False, "white")
        esc_rect = esc_surf.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.app.screen.blit(esc_surf, esc_rect)

        pg.display.flip()


    async def run(self) -> None:
        while self.running:
            self.app.clock.tick(FPS)
            self.handle_events()
            self.update_cursor()
            self.draw()
        await asyncio.sleep(0)

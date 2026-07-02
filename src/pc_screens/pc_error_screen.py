import asyncio
import pygame as pg
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pc_app import App

from pc_constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS
from pc_screens import BaseScreen, ScreenTypes
from pc_screens.pc_utils import wrap_text


class ErrorScreen(BaseScreen):
    def __init__(self, app: "App") -> None:
        self.app = app

    async def run(self) -> None:
        # global g_error_txt

        font = self.app.small_font
        text_rect = pg.Rect(
            5, 5, SCREEN_WIDTH - 10, SCREEN_HEIGHT - font.get_height() * 2
        )
        lines = wrap_text(self.app.err_msg, font, text_rect.width - 15)

        line_height = font.get_linesize() + 4
        scroll_y = 0
        max_scroll = max(0, len(lines) * line_height - text_rect.height)

        running = True
        while running:
            self.app.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    # self.app.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                        self.app.move_to(ScreenTypes.MAIN_MENU)
                    elif event.key == pg.K_DOWN or event.key == pg.K_s:
                        scroll_y = min(scroll_y + line_height, max_scroll)
                    elif event.key == pg.K_UP or event.key == pg.K_w:
                        scroll_y = max(scroll_y - line_height, 0)
                if event.type == pg.MOUSEWHEEL:
                    scroll_y = max(
                        0, min(scroll_y - event.y * line_height, max_scroll)
                    )

            self.app.screen.fill("black")
            pg.draw.rect(self.app.screen, "yellow", text_rect, 2)

            old_clip = self.app.screen.get_clip()
            self.app.screen.set_clip(text_rect)

            y = text_rect.y + 10 - scroll_y
            for line in lines:
                line_surf = font.render(line, True, "yellow")
                self.app.screen.blit(line_surf, (text_rect.x + 10, y))
                y += line_height

            self.app.screen.set_clip(old_clip)

            hint = font.render("ESC: back | UP/DOWN or mouse wheel: scroll",
                               True, "white")
            self.app.screen.blit(hint, (10, SCREEN_HEIGHT - font.get_height()))

            pg.display.flip()

            await asyncio.sleep(0)

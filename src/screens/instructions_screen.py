import asyncio
import pygame as pg

from src.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS
from src.screens import BaseScreen, ScreenTypes
from src.config import Config
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.app import App


class InstructionsScreen(BaseScreen):
    def __init__(self, config: Config, app: "App"):
        from src.app import App
        self.config: Config = config
        self.app: App = app
        self.text: str = (
            "Basic Rules:\n- Press the corresponding direction (Up, Down, " +
            "Left, Right / W, A, S, D) to steer Pac-Man through the maze.\n" +
            "- Eat the pacgums: Clear the maze of all small dots placed in " +
            "most corridors to progress to the next level.\n" +
            "- Super-pacgums: Eat the power pellets (larger dots) in the " +
            "corners. This causes the ghosts for a short time to turn blue " +
            "and run away, allowing you to gobble them up for points.\n" +
            "- Avoid the Ghosts: If a ghost touches you while they are " +
            "normal-colored, you lose a life. You start with " +
            f"{app.config.lives} lives.\n" +
            "- Eat Fruit: Bonus fruits appear twice per level in the center " +
            "of the screen, offering extra points.\n\n" +
            f"Scoring Points:\n- Pacgums: {app.config.points_per_pacgum}" +
            " points each\n" +
            f"- Super-pacgums: {app.config.points_per_super_pacgum}" +
            " points each\n" +
            f"- Ghosts: {app.config.points_per_ghost} points each\n" +
            "- Fruits: Range from 100 points (Cherry) up to 5,000 points " +
            "(Key) in higher levels."
        )

    @staticmethod
    def wrap_text(text: str, font: pg.Font, max_width: int) -> list[str]:
        """Return a list of lines wrapped to max_width."""
        lines: list[str] = []
        paragraphs = text.strip().split("\n")

        for paragraph in paragraphs:
            if paragraph.strip() == "":
                lines.append("")
                continue

            words = paragraph.split(" ")
            current_line = words[0]

            for word in words[1:]:
                test_line = current_line + " " + word
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word

            lines.append(current_line)

        return lines

    async def run(self):
        font = pg.font.SysFont("carlito", 30)
        text_rect = pg.Rect(
            5, 5, SCREEN_WIDTH - 10, SCREEN_HEIGHT - font.get_height() * 2
        )
        lines = self.wrap_text(self.text, font, text_rect.width - 15)

        line_height = font.get_linesize() + 4
        scroll_y = 0
        max_scroll = max(0, len(lines) * line_height - text_rect.height)

        running = True
        while running:
            self.app.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.app.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                        self.app.move_to(ScreenTypes.MAIN_MENU)
                    elif event.key == pg.K_DOWN:
                        scroll_y = min(scroll_y + line_height, max_scroll)
                    elif event.key == pg.K_UP:
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

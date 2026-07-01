import asyncio
import pygame as pg
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pc_app import App

from pc_constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS
<<<<<<< HEAD:src/pc_screens/pc_instructions_screen.py
from pc_screens import BaseScreen, ScreenTypes
from pc_screens.pc_utils import wrap_text
=======
from screens import BaseScreen, ScreenTypes
from screens.utils import wrap_text
>>>>>>> main:src/screens/instructions_screen.py


class InstructionsScreen(BaseScreen):
    def __init__(self, app: "App") -> None:
        self.app = app

        self.text: str = ""
        if app.config.cheat:
            self.text = (
                "You are in CHEAT mode! "
                "Available features:\n"
                "1 - Invincibility (no life lost; "
                "ghosts cannot eat the player).\n"
                "2 - Level skip (immediately win the current level).\n"
                "3 - Ghost freeze (ghosts stop moving).\n"
                "4 - Extra lives (add extra lives to the player).\n"
                "5 - Increased speed (player moves faster).\n"
                "6 - Decreased speed (player moves slower).\n"
                "7 - Change ghost mode.\n\n"
            )
        self.text += (
            "Focus on navigating a maze to eat all the dots"
            " (Pellets) while avoiding ghosts. "
            "By eating large dots (Power Pellets), "
            "you turn the ghosts blue and vulnerable "
            "to being eaten for extra points.\n\n"

            "Basic Rules:\n"
            "- Press the corresponding direction (Up, Down, "
            "Left, Right / W, A, S, D) to steer Pac-Man through the maze.\n"
            "- Eat the pacgums: Clear the maze of all small dots placed in "
            "most corridors to progress to the next level.\n"
            "- Super-pacgums: Eat the power pellets (larger dots) in the "
            "corners. This causes the ghosts for a short time to turn blue "
            "and run away, allowing you to gobble them up for points.\n"
            "- Avoid the Ghosts: If a ghost touches you while they are "
            "normal-colored, you lose a life. You start with "
            f"{app.config.lives} lives.\n"
            "- Eat Fruit: Bonus fruits appear twice per level of the screen,"
            " offering extra points.\n\n"
            f"Scoring Points:\n- Pacgums: {app.config.points_per_pacgum}"
            " points each\n"
            f"- Super-pacgums: {app.config.points_per_super_pacgum}"
            " points each\n"
            f"- Ghosts: {app.config.points_per_ghost} points each\n"
            "- Fruits: Range from 100 points (Cherry) up to 5,000 points "
            "(Key) in higher levels.\n"
        )

    async def run(self) -> None:
        font = self.app.small_font
        text_rect = pg.Rect(
            5, 5, SCREEN_WIDTH - 10, SCREEN_HEIGHT - font.get_height() * 2
        )
        lines = wrap_text(self.text, font, text_rect.width - 15)

        line_height = font.get_linesize() + 4
        scroll_y = 0
        max_scroll = max(0, (1 + len(lines)) * line_height - text_rect.height)

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
                    elif event.key == pg.K_DOWN:
                        scroll_y = min(scroll_y + line_height, max_scroll)
                    elif event.key == pg.K_UP:
                        scroll_y = max(scroll_y - line_height, 0)
                if event.type == pg.MOUSEWHEEL:
                    scroll_y = max(
                        0, min(scroll_y - event.y
                               * line_height, max_scroll)
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

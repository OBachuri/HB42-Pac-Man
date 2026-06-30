"""
---
requires-python = ">=3.10"
dependencies = [
    "pygame-ce",
    "mazegenerator",
]
---
"""

import asyncio
import sys
from typing import Any

g_error_txt: str = ""

try:
    import pygame as pg
#    from src.pc_game import Game
#    from src.pc_artifact import Pellet
except ModuleNotFoundError as e:
    g_error_txt = (f"\nError: One of the dependencies is missing\n{e}\n"
                   "Please run 'make install'\n")
    print(g_error_txt, file=sys.stderr)
#    sys.exit(1)  # can't use with pygbag


async def run_error(screen: Any, clock: Any) -> None:
    # The game loop must reside inside an async function
    # global g_error_txt

    running = True
    # font = pg.font.SysFont(['Nimbus Mono PS', 'couriernew', 'arial'], 20)
    font = pg.font.Font(None, 20)

    while running:
        events = (pg.get_event_loop()
                  if hasattr(pg, "get_event_loop")
                  else pg.event.get()
                  )
        for event in events:
            # Standard pygame event fetching fallback
            if event.type == pg.QUIT:
                running = False

        # Draw a green screen
        screen.fill((34, 139, 34))
        screen.blit(font.render(
            'PacMan 42 - game start error:', False, (10, 10, 20)),
            (10, 10))
        screen.blit(font.render(
            g_error_txt, False, (10, 10, 20)),
            (10, 40))

        pg.draw.circle(screen,
                       'yellow',
                       (200, 200), 20)
        pg.draw.circle(screen,
                       'black',
                       (192, 195), 4)
        pg.draw.circle(screen,
                       'black',
                       (208, 195), 4)
        pg.draw.rect(screen, 'black',
                             (191, 207, 18, 4), 2)
        pg.draw.circle(screen,
                       'red',
                       (220, 300), 10)
        pg.draw.circle(screen,
                       'pink',
                       (100, 330), 10)
        pg.draw.circle(screen,
                       'blue',
                       (300, 230), 10)
        pg.draw.circle(screen,
                       'orange',
                       (150, 250), 10)
        pg.display.flip()

        # Maintain 60 FPS
        clock.tick(60)

        # CRITICAL: This yields control back to the browser
        # missing this will freeze the browser window!
        await asyncio.sleep(0)


def main() -> None:
    global MazeGenerator
    global g_error_txt

    if g_error_txt == "":

        # Initialize pygame normally

        try:
            from mazegenerator.mazegenerator import MazeGenerator
            from pc_parser import Parser
            from src.pc_app import App
            # from pc_game import Game

        except Exception as ex:
            g_error_txt += f"\n Error: {ex}\n"

        if g_error_txt != "":
            g_error_txt += f"\n Platform: {sys.platform} "
            pg.init()
            pg.font.init()

            try:
                pg.mixer.init()
            except Exception as ex:
                print("Error:", ex)
                g_error_txt += f"\n Error: {ex}\n"

            screen = pg.display.set_mode((640, 480))
            clock = pg.time.Clock()
            asyncio.run(run_error(screen, clock))
        else:
            config = Parser.get_config_web()
            # config.print()
            app = App(config)
            # Run the async loop
            asyncio.run(app.run())


main()

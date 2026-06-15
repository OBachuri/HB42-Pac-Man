"""
---
requires-python = ">=3.12"
dependencies = [
    "pygame-ce",
    "mazegenerator",
]
---
"""

import asyncio
import sys

# from typing import cast
# import os
# import pygame as pg

g_error_txt: str = ""

try:
    import pygame as pg
except ModuleNotFoundError as e:
    g_error_txt = (f"\nError: One of the dependencies is missing\n{e}\n"
                   "Please run 'make install'\n")
    print(g_error_txt, file=sys.stderr)
#    sys.exit(1)  # can't use with pygbag


async def load_web_dependencies():
    # Create an async function to handle the web installation
    if sys.platform == "emscripten":
        # This import is safe here because it only triggers in the browser
        import micropip
        await micropip.install("lib/mazegenerator-00001-py3-none-any.whl")


async def run(screen, clock):
    # The game loop must reside inside an async function

    global MazeGenerator
    global g_error_txt

    try:
        from mazegenerator.mazegenerator import MazeGenerator
    except Exception as ex:
        g_error_txt += f"\n Error: {ex}\n"

    g_error_txt += f"\n Platform: {sys.platform} "

    running = True
    # font = pg.font.SysFont(['Nimbus Mono PS', 'couriernew', 'arial'], 20)
    font = pg.font.Font(None, 20)

    while running:
        for event in pg.get_event_loop() if hasattr(pg, "get_event_loop") else pg.event.get():
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


def main():
    # Initialize pygame normally
    pg.init()
    pg.font.init()
    pg.mixer.init()

    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()

    asyncio.run(run(screen, clock))


main()

# Run the async loop
# asyncio.run(main())

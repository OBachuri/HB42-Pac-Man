from __future__ import annotations

import pygame as pg
import os
import random
import asyncio

# import sys
# sys.path.append(os.path.dirname(__file__))

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from pc_map import Map
from pc_player import Player
from pc_npc import NPC, RedGhosts  # , GhostMode
from pc_artifact import PC_Artifacts
from pc_artifact import PowerPellet, Pellet
from pc_entity import FrameType
from screens import ScreenTypes


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from config import Config
    from config_web import ConfigWeb
    from src.app import App


class Game:
    def __init__(self, app: "App", config: Config | ConfigWeb | None = None):
        self.app = app
        # pg.mouse.set_visible(False)
        if app.screen:
            self.screen = app.screen
        else:
            self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        if app.clock:
            self.clock = app.clock
        else:
            self.clock = pg.time.Clock()
        if config is None:
            self.config = app.config
        else:
            self.config = config
        self.delta_time = 1
        self.game_time: float = 110   # sec
        self.global_trigger = False
        # self.global_event = pg.USEREVENT + 0
        self.global_event = pg.event.custom_type()
        self.score: int = 0
        self.level: int = 1
        self.fps: int = FPS
        self.gost_edible: int = 17  # sec - frightened time
        self.pause: bool = True
        self.runing: bool = True
        self.animation_timer: float = 0
        # pg.event.set_grab(True)
        # pg.time.set_timer(self.global_event, 40)

        # fonts
        path_ = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "inc/fonts/PressStart2P-Regular.ttf",
            )
        if os.path.exists(path_):
            self.font = pg.font.SysFont(path_, 40)
        else:
            print(f"The file with font does not exist: {path_} .")
            self.font = pg.font.SysFont('Nimbus Mono PS', 20)
        # print(path_)

        self.npcs: list[NPC] = []
        self.artifacts: list[PC_Artifacts] = []
        Pellet.sound_init()
        self.new_game()

    def new_game(self) -> None:
        self.map = Map(self)
        self.player = Player(self)

        # Add Ghost
        self.npcs.append(RedGhosts(self))
        pink = NPC(self, (self.map.cols - 1, 0),
                   (240, 24, 140), "Pink gost (Speedy)")
        self.npcs.append(pink)
        pink.read_frames_from_file("inc/img/pink/run/", FrameType.RUN)

        cyan = NPC(self,
                   (self.map.cols - 1, self.map.rows - 1),
                   (100, 250, 250), "Cyan gost (Inky, Bashful)")
        self.npcs.append(cyan)
        cyan.read_frames_from_file("inc/img/cyan/run/", FrameType.RUN)

        orange = NPC(self,
                     (0, self.map.rows - 1),
                     (250, 120, 10), "Orange gost (Clyde, Pockey)")
        self.npcs.append(orange)
        orange.read_frames_from_file("inc/img/orange/run/", FrameType.RUN)

        # print("-new-game")

        self.next_level(0)

    def next_level(self, next: int = 1) -> None:
        # global MazeGenerator
        global g_error_txt

        self.pause = True
        self.runing = True

        self.level += next
        max_level = 0
        max_level = max({l_.number for l_ in self.config.levels})

        if self.level > max_level:
            # End of all Levels = Win of game
            # change to ScreenTypes.VICTORY or GAME OVER !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.app.move_to(ScreenTypes.MAIN_MENU)
            self.pause = True
            self.runing = False
            return

        max_level = 0
        max_level = max(
            {l_.number
             for l_ in self.config.levels if l_.number <= self.level})

        l_config = []
        l_config = [lv for lv in self.config.levels if lv.number == max_level]

        if len(l_config) < 1:
            g_error_txt += f"No config for level {self.level}!"
            print(g_error_txt)
            # change to ScreenTypes.ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.app.move_to(ScreenTypes.MAIN_MENU)
            self.pause = True
            self.runing = False
            return

        config = l_config[0]

        if config.map_filename:
            self.map.get_map_form_file(config.map_filename)
            if config.remove_deadends:
                self.map.del_deadends()
        else:
            from mazegenerator.mazegenerator import MazeGenerator
            maze_ = MazeGenerator(
                size=config.size,
                exit_cell=(0, 1),
                seed=config.seed).maze
            if config.remove_deadends:
                maze_ = self.map.do_not_perfect(maze_)
            self.map.get_map(maze_)

        self.map.print()

        pg.display.set_mode(
            (max(self.map.cols*self.map.step
             + self.map.wall_thickness, SCREEN_WIDTH),
             max((self.map.rows + 3)*(self.map.step), SCREEN_HEIGHT)))

        # PacMan - place in the center
        self.player.dx = 0
        self.player.dy = 0
        self.player.teleport()

        # Set NPC
        for i in range(0, len(self.npcs)):
            n = self.npcs[i]
            if i == 1:
                n.start_x = self.map.cols - 1
                n.start_y = 0
            elif i == 2:
                n.start_x = self.map.cols - 1
                n.start_y = self.map.rows - 1
            elif i == 3:
                n.start_x = 0
                n.start_y = self.map.rows - 1
            n.reset()
            n.goal = (self.player.x, self.player.y)

        #  Add Artifacts - PowerPellet and Pellet
        self.artifacts.append(PowerPellet(self, (0, 0)))
        self.artifacts.append(PowerPellet(self, (self.map.cols - 1, 0)))
        self.artifacts.append(PowerPellet(
            self, (self.map.cols - 1, self.map.rows - 1)))
        self.artifacts.append(PowerPellet(self, (0, self.map.rows - 1)))

        place_set = {(x, y) for x in range(0, self.map.cols)
                     for y in range(0, self.map.rows)
                     if (self.map.world_map.get((x, y), 0) & 15 != 15)}

        for a_ in self.artifacts:
            place_set.remove((a_.x, a_.y))

        if config.pacgum <= 0:
            for s_ in place_set:
                self.artifacts.append(Pellet(self, s_))
        else:
            for p in range(0, config.pacgum):
                if (len(place_set) < 1):
                    print("All Pellets can't be placed "
                          f"({p+1} from {config.pacgum}).")
                    break
                x, y = random.choice(tuple(place_set))
                self.artifacts.append(Pellet(self, (x, y)))
                place_set.remove((x, y))

        self.game_time = config.level_max_time

    def update(self) -> None:
        if self.pause:
            return
        self.player.update()
        for npc in self.npcs:
            npc.update()
        for pellet in self.artifacts:
            pellet.update()
        # self.raycasting.update()
        # self.object_handler.update()
        # self.weapon.update()
        self.delta_time = self.clock.tick(self.fps)
        self.game_time -= self.delta_time / 1000
        pg.display.set_caption('Pac-man  42 '
                               f'(fps:{self.clock.get_fps(): 6.1f})')
        if len(self.artifacts) <= 0:
            self.next_level()

    def draw(self) -> None:
        self.screen.fill('black')
        self.map.draw()
        for pellet in self.artifacts:
            pellet.draw()
        self.player.draw()
        for npc in self.npcs:
            npc.draw()

        if self.pause:
            if int(self.animation_timer) % 2 == 0:
                w = self.screen.get_width()
                h = self.screen.get_height()
                surf = self.font.render(
                    "PRESS SPACE - to run \nESC - to return to the menu",
                    color=(255, 255, 255), antialias=True)
                self.screen.blit(surf, ((w - surf.get_width()) // 2, h // 2))
            self.animation_timer += 0.15/self.fps

        else:
            self.screen.blit(self.font.render(
                'Move:  W A S D, Stop: Space, Exit: Esc',
                False, (10, 10, 200)),
                (10, 10 + self.map.top + (self.map.rows)
                 * (self.map.step)))

        self.screen.blit(self.font.render(
            f'Time: {self.game_time: 3.0f}s, '
            f'Lives:{self.player.lives: 2}, '
            f'Level:{self.level: 2}, '
            f'Score:{self.score: 3}',
            False, (200, 200, 200)),
            (10, 8))
        pg.display.flip()

    def check_events(self) -> None:
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                         and event.key == pg.K_ESCAPE):
                # pg.quit()
                # sys.exit()
                self.runing = False
            elif event.type == self.global_event:
                self.global_trigger = True
            elif self.pause and (event.type == pg.KEYDOWN
                                 and (
                                     event.key == pg.K_SPACE
                                     or event.key == pg.K_w
                                     or event.key == pg.K_UP
                                     or event.key == pg.K_s
                                     or event.key == pg.K_DOWN
                                     or event.key == pg.K_a
                                     or event.key == pg.K_LEFT
                                     or event.key == pg.K_d
                                     or event.key == pg.K_RIGHT
                                     )
                                 ):
                self.pause = False

    async def run(self) -> None:
        #        pg.time.set_timer(self.global_event, 40)
        pg.display.set_caption('Pac-man 42')
        while self.runing:
            self.check_events()
            self.update()
            self.draw()
            await asyncio.sleep(0)
        self.pause = True
        self.runing = True
        self.app.move_to(ScreenTypes.MAIN_MENU)

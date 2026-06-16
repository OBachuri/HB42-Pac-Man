from __future__ import annotations

import pygame as pg
# import sys
import os
import random
import asyncio

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from pc_map import Map
from pc_player import Player
from pc_npc import NPC, RedGhosts  # , GhostMode
from pc_artifact import PC_Artifacts
from pc_artifact import PowerPellet, Pellet
# from src.config import Config
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
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.game_time = 110   # sec
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        self.score = 0
        self.level = 1
        self.fps = FPS
        self.gost_edible = 17  # sec - frightened time
        self.pause = True
        self.runing = True
        pg.time.set_timer(self.global_event, 40)
        self.config = config
        self.animation_timer: float = 0

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
        self.new_game()
        Pellet.sound_init()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        print(self.config)
        # self.npcs.append(RedGhosts(self))
        # print("-new-game")

        #  self.npcs = [NPC(self), NPC(self), NPC(self), NPC(self)]

    def next_level(self):

        pacgum = -111

        self.level += 1
        self.game_time = 110   # sec

        # Set pleer in the center
        self.player.dx = 0
        self.player.dy = 0
        self.player.teleport()

        # Set NPC
        for n in self.npcs:
            n.reset()

        #  Add PowerPellet and Pellet
        self.artifacts.append(PowerPellet(self, (0, 0)))
        self.artifacts.append(PowerPellet(self, (self.map.cols - 1, 0)))
        self.artifacts.append(PowerPellet(self,
                                          (self.map.cols - 1,
                                           self.map.rows - 1)))
        self.artifacts.append(PowerPellet(self, (0, self.map.rows - 1)))

        place_set = {(x, y) for x in range(0, self.map.cols)
                     for y in range(0, self.map.rows)
                     if (self.map.world_map.get((x, y), 0) & 15 != 15)}

        for a_ in self.artifacts:
            place_set.remove((a_.x, a_.y))

        if pacgum <= 0:
            for s_ in place_set:
                self.artifacts.append(Pellet(self, s_))
        else:
            for p in range(0, pacgum):
                if (len(place_set) < 1):
                    print("All Pellets can't be placed",
                          f"({p+1} from {pacgum}).")
                    break
                x, y = random.choice(tuple(place_set))
                self.artifacts.append(Pellet(self, (x, y)))
                place_set.remove((x, y))

    def update(self):
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

    def draw(self):
        # self.screen.fill('black')
        self.screen.fill('red')
        # self.map.draw()
        # for pellet in self.artifacts:
        #     pellet.draw()
        # self.player.draw()
        # for npc in self.npcs:
        #     npc.draw()

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

    def check_events(self):
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

            # self.player.single_fire_event(event)

    async def run(self):
        while self.runing:
            self.check_events()
            self.update()
            self.draw()
            await asyncio.sleep(0)
        self.pause = True
        self.runing = True
        self.app.move_to(ScreenTypes.MAIN_MENU)

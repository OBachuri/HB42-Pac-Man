from __future__ import annotations

import pygame as pg
import random
import asyncio
from collections.abc import Sequence


# import sys
# sys.path.append(os.path.dirname(__file__))

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from pc_map import Map
from pc_player import Player
from pc_npc import NPC, RedGhosts  # , GhostMode
from pc_artifact import PC_Artifacts
from pc_artifact import PowerPellet, Pellet, BonusFruitType, Fruit
from pc_entity import FrameType
from screens import ScreenTypes


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from config import Config
    from config_web import ConfigWeb
    from app import App


class Game:
    def __init__(self, app: "App", config: Config | ConfigWeb | None = None):
        self.app = app
        # pg.mouse.set_visible(False)
        if app.screen:
            self.screen = app.screen
        else:
            self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_left_shift: int = 0
        if app.clock:
            self.clock = app.clock
        else:
            self.clock = pg.time.Clock()
        if config is None:
            self.config = app.config
        else:
            self.config = config
        self.delta_time = 1
        self.game_max_time: float = 110   # sec
        self.game_time: float = self.game_max_time   # sec
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
        self.fruits_triger: list[int] = []
        self.points_per_bonus_fruit: int = 100
        self.bonus_fruit_type: BonusFruitType = BonusFruitType.CHERRY
        self.old_keys: Sequence[bool] = pg.key.get_pressed()

        # pg.event.set_grab(True)
        # pg.time.set_timer(self.global_event, 40)

        self.font = app.small_font

        self.npcs: list[NPC] = []
        self.artifacts: list[PC_Artifacts] = []
        Pellet.sound_init()
        Fruit.sound_init()
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
        pink.read_frames_from_file("inc/img/pink/stay/", FrameType.STAY)

        cyan = NPC(self,
                   (self.map.cols - 1, self.map.rows - 1),
                   (100, 250, 250), "Cyan gost (Inky, Bashful)")
        self.npcs.append(cyan)
        cyan.read_frames_from_file("inc/img/cyan/run/", FrameType.RUN)
        cyan.read_frames_from_file("inc/img/cyan/stay/", FrameType.STAY)

        orange = NPC(self,
                     (0, self.map.rows - 1),
                     (250, 120, 10), "Orange gost (Clyde, Pockey)")
        self.npcs.append(orange)
        orange.read_frames_from_file("inc/img/orange/run/", FrameType.RUN)
        orange.read_frames_from_file("inc/img/orange/stay/", FrameType.STAY)

        self.player.lives = self.config.lives

        # print("-new-game")

        self.next_level(0)

    def next_level(self, next: int = 1) -> None:
        # global MazeGenerator

        self.pause = True
        self.runing = True

        self.level += next
        max_level = 0
        max_level = max({l_.number for l_ in self.config.levels})

        if self.level > max_level:
            # End of all Levels = Win of game
            self.app.move_to(ScreenTypes.END_OF_GAME)
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
            self.app.err_msg = f"ERROR: No config for level {self.level}!"
            print(self.app.err_msg)
            self.app.move_to(ScreenTypes.ERROR)
            self.pause = True
            self.runing = False
            return

        config = l_config[0]

        self.artifacts = []

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

        self.screen_left_shift = 0
        if ((self.map.cols*self.map.step
             + self.map.wall_thickness) < SCREEN_WIDTH):
            self.screen_left_shift = (SCREEN_WIDTH
                                      - self.map.cols*self.map.step
                                      - self.map.wall_thickness) // 2
        # PacMan - place in the center
        self.player.dx = 0
        self.player.dy = 0
        self.player.teleport()

        self.player.speed_factor = config.speed_factor_player
        self.player.max_d = config.max_player_acceleration

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
            n.speed_factor = config.speed_factor_ghost
            n.points = self.config.points_per_ghost

        #  Add Artifacts - PowerPellet and Pellet
        self.artifacts.append(
            PowerPellet(self, (0, 0),
                        points=self.config.points_per_super_pacgum))
        self.artifacts.append(
            PowerPellet(self, (self.map.cols - 1, 0),
                        points=self.config.points_per_super_pacgum))
        self.artifacts.append(PowerPellet(
            self, (self.map.cols - 1, self.map.rows - 1),
            points=self.config.points_per_super_pacgum))
        self.artifacts.append(PowerPellet(
            self, (0, self.map.rows - 1),
            points=self.config.points_per_super_pacgum))

        place_set = {(x, y) for x in range(0, self.map.cols)
                     for y in range(0, self.map.rows)
                     if (self.map.world_map.get((x, y), 0) & 15 != 15)}

        for a_ in self.artifacts:
            place_set.remove((a_.x, a_.y))

        if config.pacgum <= 0:
            for s_ in place_set:
                self.artifacts.append(Pellet(
                    self, s_, points=self.config.points_per_pacgum))
        else:
            for p in range(0, config.pacgum):
                if (len(place_set) < 1):
                    print("All Pellets can't be placed "
                          f"({p+1} from {config.pacgum}).")
                    break
                x, y = random.choice(tuple(place_set))
                self.artifacts.append(
                    Pellet(self, (x, y),
                           points=self.config.points_per_pacgum))
                place_set.remove((x, y))

        # ======== Bonus Fruits
        # Fill array with pellets quantity when bonus fruit must be created.
        # Bonus fruit appears two times for every level:
        # when 30% and 70% of Pacgum are eaten

        self.fruits_triger = []
        pellets_cnt = len(self.artifacts)

        if (pellets_cnt > 9) and (config.points_per_bonus_fruit > 0):
            self.fruits_triger = [int(0.7 * pellets_cnt),
                                  int(0.3 * pellets_cnt)]
            self.points_per_bonus_fruit = config.points_per_bonus_fruit
            self.bonus_fruit_type = config.bonus_fruit_type

        self.game_max_time = config.level_max_time
        self.game_time = self.game_max_time

    def update(self) -> None:
        if self.pause:
            self.delta_time = self.clock.tick(self.fps)
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
        # check for end of time
        if self.game_time <= 0:
            self.game_time = 0
            if self.player.alive:
                self.player.frame_index = 0
            self.player.alive = False
        cheat = ""
        if self.config.cheat:
            cheat = "(CHEAT MODE)"
        pg.display.set_caption(f'Pac-man 42 {cheat}'
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
            txt_ = "\n PRESS SPACE - to run \n ESC - to return to the menu \n "
            if int(self.animation_timer) % 2 == 0:
                w = self.screen.get_width()
                h = self.screen.get_height()
                surf = self.font.render(
                    txt_,
                    color='yellow', bgcolor=(10, 10, 0, 40), antialias=True)
                self.screen.blit(surf, ((w - surf.get_width()) // 2, h // 2))
            self.animation_timer += 1/self.fps
            txt_ = "PRESS SPACE - to run \nESC - to return to the menu \n "
            self.screen.blit(self.font.render(
                txt_,
                False, (10, 10, 200)),
                (10, 10 + self.map.top + (self.map.rows)
                 * (self.map.step)))

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
                self.app.move_to(ScreenTypes.MAIN_MENU)
                self.runing = False
                return
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
            if event.type == pg.KEYDOWN and self.config.cheat:
                keys = pg.key.get_pressed()
                if self.old_keys != keys:
                    self.old_keys = keys
                    if keys[pg.K_1]:    # invincibility
                        self.player.invincibil = not (self.player.invincibil)
                    if keys[pg.K_2]:    # skip level
                        self.next_level()
                    if keys[pg.K_4]:    # Extra lives to the player
                        self.player.lives += 1
                    if keys[pg.K_5]:    # Increased speed - player moves faster
                        self.player.speed_factor = min(
                            self.player.speed_factor + 0.005,
                            0.3 / self.player.max_d)
                    if keys[pg.K_6]:    # Increased speed - player moves faster
                        self.player.speed_factor = max(
                            self.player.speed_factor - 0.01,
                            0.005 / self.player.max_d)

            else:
                self.old_keys = pg.key.get_pressed()

    async def run(self) -> None:
        #        pg.time.set_timer(self.global_event, 40)
        pg.display.set_caption('Pac-man 42')
        if self.player.lives < 1:
            self.score = 0
            self.level = 1
            self.player.lives = self.config.lives
            self.next_level(0)
        while self.runing:
            self.check_events()
            self.update()
            self.draw()
            await asyncio.sleep(0)
        self.pause = True
        self.runing = True
        # self.app.move_to(ScreenTypes.MAIN_MENU)

from __future__ import annotations

import pygame as pg
import random
from collections.abc import Sequence
# from enum import Enum
from pc_entity import Entity, FrameType, GhostMode
from pc_sound import SoundType  # , Sound
from pc_constants import FPS
from pc_npc import NPC

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pc_game import Game


class RedGhost(NPC):
    """ Red ghost (Blinky, Shadow)
        Blinky always chase his prey :)
    """
    def __init__(self, game: Game,
                 point: tuple[float, float] = (0, 0)) -> None:
        super().__init__(game, point, (250, 20, 20),
                         "Red ghost (Blinky, Shadow)")
        self.read_frames_from_file("inc/img/red/run/", FrameType.RUN)
        self.read_frames_from_file("inc/img/red/stay/", FrameType.STAY)

    def find_goal(self) -> None:
        if self.mode == GhostMode.CHASE:
            self.goal = pg.Vector2(int(round(self.game.player.x, 0)),
                         int(round(self.game.player.y, 0)))
        else:
            super().find_goal()


class PinkGhost(NPC):
    def __init__(self, game: Game,
                 point: tuple[float, float] = (0, 0)) -> None:
        super().__init__(game, point, (240, 24, 140), "Pink ghost (Speedy)")
        self.read_frames_from_file("inc/img/pink/run/", FrameType.RUN)
        self.read_frames_from_file("inc/img/pink/stay/", FrameType.STAY)


    def find_goal(self) -> None:
        if self.mode == GhostMode.CHASE:
            pos = pg.Vector2(self.x, self.y)
            player_pos = pg.Vector2(int(round(self.game.player.x, 0)),
                                    int(round(self.game.player.y, 0)))
            player_direction = 0
            if pos.distance_to(player_pos) > self.start_chase_if_near:
                player_direction = self.get_player_direction()
            if player_direction:
                self.goal = self.adjust_vector(player_pos + player_direction * 2)
                return
            self.goal = player_pos
        else:
            super().find_goal()


class CyanGhost(NPC):
    def __init__(self, game: Game,
                 point: tuple[float, float] = (0, 0),
                 red_ghost: NPC | None = None) -> None:
        super().__init__(game, point, (100, 250, 250),
                         "Cyan ghost (Inky, Bashful)")
        self.red_ghost = red_ghost
        self.read_frames_from_file("inc/img/cyan/run/", FrameType.RUN)
        self.read_frames_from_file("inc/img/cyan/stay/", FrameType.STAY)

    def find_goal(self) -> None:
        if self.mode == GhostMode.CHASE:
            player_pos = pg.Vector2(int(round(self.game.player.x, 0)),
                                    int(round(self.game.player.y, 0)))
            red_ghost_pos = pg.Vector2(0, 0)
            if self.red_ghost:
                red_ghost_pos = pg.Vector2(int(round(self.red_ghost.x, 0)),
                                           int(round(self.red_ghost.y, 0)))

            vec1 = self.adjust_vector(player_pos + self.get_player_direction() * 2)
            vec2 = self.adjust_vector((vec1 - red_ghost_pos) * 2)
            self.goal = self.adjust_vector(red_ghost_pos + vec2)
        else:
            super().find_goal()


class OrangeGhost(NPC):
    def __init__(self, game: Game,
                 point: tuple[float, float] = (0, 0)) -> None:
        super().__init__(game, point, (250, 120, 10),
                         "Orange ghost (Clyde, Pockey)")
        self.read_frames_from_file("inc/img/orange/run/", FrameType.RUN)
        self.read_frames_from_file("inc/img/orange/stay/", FrameType.STAY)

    def find_goal(self) -> None:
        if self.mode == GhostMode.CHASE:
            tiles = int(self.game.map.cols * self.game.map.rows * 0.042)
            player_pos = pg.Vector2(int(round(self.game.player.x, 0)),
                                    int(round(self.game.player.y, 0)))
            max_x = self.game.map.cols - 1
            max_y = self.game.map.rows - 1
            # pos_x_before = (0, player_pos.x - 1)
            # pos_x_after = (player_pos.x + 1, )
            # pos_y_before = (0, player_pos.y - 1)
            # pos_y_after = (player_pos.y + 1, )
            # # self.goal = self.adjust_vector(red_ghost_pos + vec2)
            self.goal = pg.Vector2(int(round(self.game.player.x, 0)),
                         int(round(self.game.player.y, 0)))
        else:
            super().find_goal()

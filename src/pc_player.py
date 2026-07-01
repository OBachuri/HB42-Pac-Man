from __future__ import annotations

import pygame as pg
import pygame.gfxdraw as pggf
import math
# from collections.abc import Sequence

from pc_entity import Entity, FrameType
from pc_screens import ScreenTypes
from pc_sound import SoundType, Sound

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pc_game import Game


class Player(Entity):
    """ Player = PacMan """
    def __init__(self, game: Game,
                 point: tuple[float, float] = (0, 0),
                 color: tuple[int, int, int] = (250, 250, 10),
                 name: str = "PacMan", size: int = 21, lives: int = 3):

        super().__init__(game, color=color, name=name, size=size)

        self.x: float = 0
        self.y: float = 0
        self.x, self.y = point
        self.angle: float | int = 0
        self.speed_factor: float = 0.01
        self.lives: int = lives
        self.dx: int = 0
        self.dy: int = 0
        self.invincibil: bool = False
        self.frame_index: int = 0
        self.avto_shift: float = 0.25    # coefficient

        try:
            self.teleport()
        except Exception:
            pass

        self.read_frames_from_file("inc/img/pacman/run/", FrameType.RUN)
        self.read_frames_from_file("inc/img/pacman/stay/", FrameType.STAY)
        self.read_frames_from_file("inc/img/pacman/death/", FrameType.DEATH)

        self.sounds: dict[SoundType, list[Sound]] = {}
        self.sounds = Sound.read_sounds_from_files(
             "inc/sounds/pacman/death/", SoundType.EATEN, sounds=self.sounds)

    def teleport(self, x: int = -1, y: int = -1) -> None:
        if x < 0:
            x = int(self.game.map.cols / 2)
        if y < 0:
            y = int(self.game.map.rows / 2)
        while (self.game.map.world_map.get((x, y), 0) & 15 == 15) and (x > 0):
            x -= 1
        if (((x < 0) or (y < 0)
             or (x >= self.game.map.cols) or (y >= self.game.map.rows))):
            return
        self.x = int(x)
        self.y = int(y)

    def check_walls(self, new_x: float, new_y: float,
                    max_shift: float) -> bool:
        """ Returned True if there is wall on new palace """

        new_x_int = int(round(new_x, 0))
        new_y_int = int(round(new_y, 0))

        if (((abs(new_x_int - new_x) <= max_shift)
             and (abs(new_y_int - new_y) <= max_shift))):
            # We are inside the cell.
            return False

        w = self.game.map.world_map.get((new_x_int, new_y_int), 0)

        if abs(new_x_int - new_x) > max_shift:
            # We are crossing the edge of cell (left or right)
            if new_x_int > new_x:  # left
                if (w & 8):  # here is left wall
                    return True
            else:   # right
                if (w & 2):  # here is right wall
                    return True

        if abs(new_y_int - new_y) > max_shift:
            # We are crossing the edge of cell (top or bottom)
            if new_y_int > new_y:  # top
                if (w & 1):  # here is top wall
                    return True
            else:   # bottom
                if (w & 4):  # here is bottom wall
                    return True

        if (((abs(new_x_int - new_x) <= max_shift)
             or (abs(new_y_int - new_y) <= max_shift))):
            # We crossed only one edge of cell and there is no wall there.
            return False

        # We need to check Diagonal cell
        if new_x_int > new_x:  # Left
            if new_y_int > new_y:  # Top + Left
                return (bool(self.game.map.world_map.get(
                        (new_x_int - 1, new_y_int - 1), 0) & 6 > 0))
            else:  # Bottom + Left
                return (bool(self.game.map.world_map.get(
                        (new_x_int - 1, new_y_int + 1), 0) & 3 > 0))
        else:  # Right
            if new_y_int > new_y:  # Top + Right
                return (bool(self.game.map.world_map.get(
                        (new_x_int + 1, new_y_int - 1), 0) & 12 > 0))
            else:  # Bottom + Right
                return (bool(self.game.map.world_map.get(
                        (new_x_int + 1, new_y_int + 1), 0) & 9 > 0))
        return False

    def after_death(self) -> None:
        self.lives -= 1
        self.reset()
        for n in self.game.npcs:
            n.reset()
        self.game.pause = True
        self.game.game_time = self.game.game_max_time
        if self.lives <= 0:
            self.game.app.move_to(ScreenTypes.END_OF_GAME)
            self.game.running = False

    def movement(self) -> None:
        num_key_pressed = -1
        dx: int = self.dx
        dy: int = self.dy
        if self.alive:
            keys = pg.key.get_pressed()

            if keys[pg.K_w] or keys[pg.K_UP]:
                num_key_pressed += 1
                dy += -1
            if keys[pg.K_s] or keys[pg.K_DOWN]:
                num_key_pressed += 1
                dy += 1
            if keys[pg.K_a] or keys[pg.K_LEFT]:
                num_key_pressed += 1
                dx += -1
            if keys[pg.K_d] or keys[pg.K_RIGHT]:
                num_key_pressed += 1
                dx += 1
            if keys[pg.K_SPACE]:
                dx = 0
                dy = 0
                # print("---- stop ----")
            if keys[pg.K_d] or keys[pg.K_p]:
                self.angle += 1
            if keys[pg.K_d] or keys[pg.K_o]:
                self.angle -= 1

        if (self.angle >= 360):
            self.angle = 0
        elif self.angle < 0:
            self.angle = 359

        if (dx == 0) and (dy == 0):
            self.dx = dx
            self.dy = dy
            return

        max_shift = round((((self.game.map.cell_size - self.size * 2 - 2) / 2)
                           / (self.game.map.cell_size
                              + self.game.map.wall_thickness)), 10)

        old_dx = dx
        old_dy = dy

        # limit on max speed
        if abs(dx) + abs(dy) > self.max_d:
            # print("d--in(x,y)",dx,dy)
            if dx != 0:
                dx = int(round(dx * self.max_d/(abs(dx) + abs(dy)), 0))
            if dy != 0:
                dy = int(round(dy * self.max_d/(abs(dx) + abs(dy)), 0))
            # print("d-out(x,y)",dx,dy)

        dx_sf = dx * self.speed_factor
        dy_sf = dy * self.speed_factor

        new_x = self.x + dx_sf
        new_y = self.y + dy_sf

        if self.check_walls(new_x, new_y, max_shift):
            if (dx != 0) and (dy != 0):
                if abs(dx) > abs(dy):
                    if self.check_walls(new_x, self.y, max_shift):
                        if self.check_walls(self.x, new_y, max_shift):
                            dy = 0
                            new_y = self.y
                        dx = 0
                        new_x = self.x
                    else:
                        dy = 0
                        new_y = self.y
                else:
                    if self.check_walls(self.x, new_y, max_shift):
                        if self.check_walls(new_x, self.y, max_shift):
                            dx = 0
                            new_x = self.x
                        dy = 0
                        new_y = self.y
                    else:
                        dx = 0
                        new_x = self.x
            else:
                dy = 0
                new_y = self.y
                dx = 0
                new_x = self.x

        if (dy == 0) and (dx == 0):  # we cant move to new point
            # try to move to the edge
            x_int = int(round(self.x, 0))
            y_int = int(round(self.y, 0))
            w = self.game.map.world_map.get((x_int, y_int), 0)

            if (((dx_sf > 0) and (w & 2)
                 and (self.x - x_int < (max_shift - 1e-10)))):
                # move to the right but there is a wall
                new_x = x_int + max_shift - 1e-10
            elif (((dx_sf < 0) and (w & 8)
                   and (x_int - self.x < (max_shift - 1e-10)))):
                # move to the left but there is a wall
                new_x = x_int - max_shift + 1e-10
            if (((dy_sf > 0) and (w & 4)
                 and (self.y - y_int < (max_shift - 1e-10)))):
                # move to the bottom but there is a wall
                new_y = y_int + max_shift - 1e-10
            elif (((dy_sf < 0) and (w & 1)
                   and (y_int - self.y < (max_shift - 1e-10)))):
                # move to the top but there is a wall
                new_y = y_int - max_shift + 1e-10

            if (self.x == new_x) and (self.y == new_y):
                # we can't move, check if we can shift
                try:
                    shift_ = (
                        self.avto_shift * self.size / self.game.map.cell_size)
                except Exception as ex_:
                    print("Error calculating PacMan shift:", ex_)
                    shift_ = 0.0916
                if ((dx_sf > 0) and not (w & 2)):  # move right
                    if (((y_int - self.y) > 0) and (
                         (y_int - self.y) < (max_shift + shift_ - 1e-10))):
                        new_y = y_int - max_shift + 1e-10
                        dx = max(1, old_dx - 3)
                    elif (((self.y - y_int) > 0) and (
                         (self.y - y_int) < (max_shift + shift_ - 1e-10))):
                        new_y = y_int + max_shift - 1e-10
                        dx = max(1, old_dx - 3)
                elif ((dx_sf < 0) and not (w & 8)):  # move left
                    if (((y_int - self.y) > 0) and (
                         (y_int - self.y) < (max_shift + shift_ - 1e-10))):
                        new_y = y_int - max_shift + 1e-10
                        dx = min(-1, old_dx + 3)
                    elif (((self.y - y_int) > 0) and (
                         (self.y - y_int) < (max_shift + shift_ - 1e-10))):
                        new_y = y_int + max_shift - 1e-10
                        dx = min(-1, old_dx + 3)
                elif ((dy_sf > 0) and not (w & 4)):  # move down
                    if (((x_int - self.x) > 0) and (
                         (x_int - self.x) < (max_shift + shift_ - 1e-10))):
                        new_x = x_int - max_shift + 1e-10
                        dy = max(1, old_dy - 3)
                    elif (((self.x - x_int) > 0) and (
                         (self.x - x_int) < (max_shift + shift_ - 1e-10))):
                        new_x = x_int + max_shift - 1e-10
                        dy = max(1, old_dy - 3)
                elif ((dy_sf < 0) and not (w & 1)):  # move up
                    if (((x_int - self.x) > 0) and (
                         (x_int - self.x) < (max_shift + shift_ - 1e-10))):
                        new_x = x_int - max_shift + 1e-10
                        dy = min(-1, old_dy + 3)
                    elif (((self.x - x_int) > 0) and (
                         (self.x - x_int) < (max_shift + shift_ - 1e-10))):
                        new_x = x_int + max_shift - 1e-10
                        dy = min(-1, old_dy + 3)

        self.x = new_x
        self.y = new_y

        # Check edge of maze - only for error if no wall on edge of maze
        if (self.x <= - max_shift):
            self.x = - max_shift
            dx = 0
        elif (self.x >= (self.game.map.cols - 1) + max_shift):
            self.x = self.game.map.cols - 1 + max_shift
            dx = 0
        if (self.y < - max_shift):
            self.y = - max_shift
            dy = 0
        elif (self.y > (self.game.map.rows - 1) + max_shift):
            self.y = self.game.map.rows - 1 + max_shift
            dy = 0

        self.dx = dx
        self.dy = dy

        if (dx != 0) or (dy != 0):
            self.angle = math.degrees(math.atan2(-dy, dx)) % 360

        #  print(f"after - cur:({self.x},{self.y}),int:({x},{y},
        #          max_shift:{max_shift}, df({dx},{dy})")

    def draw(self) -> None:

        x = (self.x * (self.game.map.cell_size
                       + self.game.map.wall_thickness)
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness
             + self.game.screen_left_shift)

        y = (self.y * (self.game.map.cell_size
                       + self.game.map.wall_thickness)
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness
             + self.game.map.top)

        if not (self.alive):
            frames = self.frames.get(FrameType.DEATH, [])
            angle = 0
            # print("DEATH from",len(frames),self.frame_index)
        elif (self.dx == 0) and (self.dy == 0):
            frames = self.frames.get(FrameType.STAY, [])
            angle = 0
        else:
            frames = self.frames.get(FrameType.RUN, [])
            angle = int(self.angle)
        if len(frames) > 0:
            if self.frame_index >= len(frames):
                if not (self.alive):
                    self.frame_index = len(frames) - 1
                    self.after_death()
                    return
                self.frame_index = 0
            image = frames[self.frame_index]
            if angle == 0:
                frame = image
            elif (angle == 180):
                frame = pg.transform.flip(image, True, False)
            elif (angle < 260) and (angle > 90):
                frame = pg.transform.flip(image, True, False)
                frame = pg.transform.rotate(frame, angle-180)
            else:
                frame = pg.transform.rotate(image, angle)
            rect = frame.get_rect(center=(int(x), int(y)))
            self.game.screen.blit(frame, rect)
        else:
            pg.draw.circle(self.game.screen,
                           self.color,
                           (x, y), self.size)
            # eye
            # print("angle:", math.degrees(self.angle))
            sin_a = math.sin(self.angle)
            cos_a = math.cos(self.angle)
            pg.draw.circle(self.game.screen,
                           'black',
                           (x + 5 * sin_a,
                            y - 5 * cos_a
                            ), 3)
            # mouth = jaws
            pggf.pie(self.game.screen, int(x), int(y), self.size,
                     -20, 20, (255, 0, 0))

        if self.game.config.cheat:
            if self.invincibil:
                txt_ = (f'Invincibil - x:{float(self.x):.4}, '
                        f'y:{float(self.y):.4}, '
                        f's:{float(self.speed_factor):.4}')
            else:
                txt_ = f'x:{self.x}, y:{self.y}, a:{self.angle} '
            txt_ += "\n"
            for n in self.game.npcs:
                txt_ += f'{n.name[0]}:{n.mode.name} '

            self.game.screen.blit(self.game.font.render(
                txt_, False, (10, 10, 200)),
                (10, 5 + (self.game.map.rows + 1)
                 * (self.game.map.step)
                 + self.game.map.top))

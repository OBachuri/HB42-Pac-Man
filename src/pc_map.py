from __future__ import annotations

import pygame as pg
from collections import deque
import random
import os

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pc_game import Game


class Map:

    directions = {1: (0, -1), 2: (1, 0), 4: (0, 1), 8: (-1, -0)}
    possible_moves = dict((w, [d for b, d in {
        1: (0, -1), 2: (1, 0), 4: (0, 1), 8: (-1, -0)
    }.items() if not (w & b)]) for w in range(16))

    def __init__(self, game: Game):
        self.game = game
        self.world_map: dict[tuple[int, int], int] = {}
        self.rows: int = 3
        self.cols: int = 3
        self.cell_size: int = 55
        self.wall_thickness: int = 4
        self.step: int = self.cell_size + self.wall_thickness
        self.top: int = 35
        self.color: tuple[int, ...] = (40, 200, 40)
        self.background: pg.Surface | None = None

    def get_cell(self, x: int, y: int) -> int:
        return self.world_map.get((x, y), 0)

    def has_cell_exit(self, x: int, y: int) -> bool:
        # return true if the cell inside the maze and have exit
        return bool(
            x >= 0 and y >= 0
            and x < self.cols
            and y < self.rows
            and (self.get_cell(x, y) & 15) != 15)

    def get_direction_for_cell(self, x: int, y: int) -> list[tuple[int, int]]:
        w = self.world_map.get((x, y), 0) & 15
        return (list(self.possible_moves[w]))

        # l_: list[tuple[int, int]] = []
        # if w & 1 == 0:  # top
        #     l_ = [(0, -1)]
        # if w & 2 == 0:  # right
        #     l_.append((1, 0))
        # if w & 4 == 0:  #  bottom
        #     l_.append((0, 1))
        # if w & 8 == 0:  #  left
        #     l_.append((-1, 0))
        # return l_

    def get_map(self, maze_: list[list[int]]) -> None:
        # get map from list
        self.world_map = {}
        for y, row in enumerate(maze_):
            for x, value in enumerate(row):
                self.world_map[(x, y)] = value
                self.rows = 1
        self.cols = 0
        self.rows = len(maze_)
        if self.rows > 0:
            self.cols = len(maze_[0])
        self.background = None

    def get_map_form_file(self, file_name: str) -> None:
        self.world_map = {}
        y: int = 0

        if file_name[:4].lower() == 'inc/':
            file_name = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                file_name,
            )

        with open(file_name, "r", encoding="utf-8") as f:
            for line in f:
                l_ = line.strip()
                if y == 0:
                    self.cols = len(l_)
                elif len(l_) < self.cols:
                    self.rows = y
                    break
                for x in range(0, len(l_)):
                    v = int(l_[x], 16)
                    if v > 0:
                        self.world_map[(x, y)] = v
                y += 1

        error_ = self.map_check()
        if len(error_) > 0:
            print(f"Error in maze file {file_name}:")
            print("(X,Y)=Walls (Walls = 1-Top + 2-Right + 4-Bottom + 8-Left)")
            for e_ in error_:
                print(e_)
        self.background = None

    def map_check(self) -> list[str]:
        error_: list[str] = []
        for x in range(0, self.cols):
            for y in range(0, self.rows):
                w = self.world_map.get((x, y), 0)
                if (x == 0):
                    if ((w & 8) == 0):
                        # left edge of maze without wall
                        error_.append(f"({x+1},{y+1})={w}"
                                      " - left edge of maze without wall")
                        w += 8
                        self.world_map[(x, y)] = w
                else:
                    if (x + 1 == self.cols) and ((w & 2) == 0):
                        # right edge of maze without wall
                        error_.append(f"({x+1},{y+1})={w}"
                                      " - right edge of maze without wall")
                        w += 2
                        self.world_map[(x, y)] = w
                    w1 = self.world_map.get((x - 1, y), 0)
                    if ((w1 & 2) > 0) ^ ((w & 8) > 0):
                        error_.append(
                            f"({x},{y+1})={w1} and ({x+1},{y+1})={w}"
                            " - vertical wall exist only on one side")
                        if (w1 & 2) > 0:
                            w += 8
                            self.world_map[(x, y)] = w
                        else:
                            w1 += 2
                            self.world_map[(x - 1, y)] = w1

                if (y == 0):
                    if ((w & 1) == 0):
                        # top edge of maze without wall
                        error_.append(f"({x+1},{y+1})={w}"
                                      " - top edge of maze without wall")
                        w += 1
                        self.world_map[(x, y)] = w
                else:
                    w1 = self.world_map.get((x, y - 1), 0)
                    if ((w1 & 4) > 0) ^ ((w & 1) > 0):
                        error_.append(
                            f"({x+1},{y})={w1} and ({x+1},{y+1})={w}"
                            " - horizontal wall exist only on one side")
                        if (w1 & 4) > 0:
                            w += 1
                            self.world_map[(x, y)] = w
                        else:
                            w1 += 4
                            self.world_map[(x, y - 1)] = w1
                    if (y + 1 == self.rows) and ((w & 4) == 0):
                        # bottom edge of maze without wall
                        error_.append(f"({x+1},{y+1})={w}"
                                      " - bottom edge of maze without wall")
                        w += 4
                        self.world_map[(x, y)] = w

        return (error_)

    def find_path(self,
                  start: tuple[int, int] = (0, 0),
                  end: tuple[int, int] = (0, 0)) -> list[tuple[int, int]]:

        path_: list[tuple[int, int]] = []

        if start == end:
            return path_

        height = self.rows
        width = self.cols

        queue = deque([start])
        visited = set([start])
        parent: dict[tuple[int, int], tuple[int, int]] = {}

        while queue:
            x, y = queue.popleft()

            if (x, y) == end:
                # reconstruct path
                while (x, y) != start:
                    path_.append((x, y))
                    x, y = parent[(x, y)]
                path_.append((start[0], start[1]))
                path_.reverse()
                return path_

            cell = self.world_map.get((x, y), 0) & 15

            # ----- TOP -----
            if not (cell & 1):  # no top wall
                nx, ny = x, y - 1
                if 0 <= ny < height and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

            # ----- RIGHT -----
            if not (cell & 2):  # no right wall
                nx, ny = x + 1, y
                if 0 <= nx < width and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

            # ----- BOTTOM -----
            if not (cell & 4):  # no bottom wall
                nx, ny = x, y + 1
                if 0 <= ny < height and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

            # ----- LEFT -----
            if not (cell & 8):  # no left wall
                nx, ny = x - 1, y
                if 0 <= nx < width and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))
        return path_

    def draw(self) -> None:
        # if self.background is None:
        pg.draw.rect(self.game.screen, self.color, (
            self.game.screen_left_shift, self.top,
            self.wall_thickness,
            self.rows * self.step
            + self.wall_thickness), 0)
        pg.draw.rect(self.game.screen, self.color, (
            self.game.screen_left_shift, self.rows * self.step
            + self.top,
            self.cols * self.step,
            self.wall_thickness), 0)

        for pos in self.world_map:
            w = self.world_map[pos] & 15
            if w == 15:  # call is part of 42 pattern (isolated cell)
                pg.draw.rect(self.game.screen, 'white', (
                    self.game.screen_left_shift
                    + pos[0] * self.step
                    + self.wall_thickness,
                    pos[1] * self.step
                    + self.top + self.wall_thickness,
                    self.cell_size,
                    self.cell_size), 0)
            if (w & 2) == 2:
                pg.draw.rect(self.game.screen, self.color, (
                    self.game.screen_left_shift
                    + (pos[0] + 1) * self.step,
                    pos[1] * self.step
                    + self.top,
                    self.wall_thickness,
                    self.cell_size + self.wall_thickness * 2), 0)
            if (w & 1) == 1:
                pg.draw.rect(self.game.screen, self.color, (
                    self.game.screen_left_shift
                    + pos[0] * self.step,
                    pos[1] * self.step
                    + self.top,
                    self.cell_size + self.wall_thickness * 2,
                    self.wall_thickness), 0)
        self.background = self.game.screen.copy()
        # else:
        #     self.game.screen.blit(self.background)

    def del_deadends(self) -> None:
        maze: list[list[int]] = []
        for y in range(0, self.rows):
            l_ = []
            for x in range(0, self.cols):
                l_.append(self.world_map.get((x, y), 0))
            maze.append(l_)
        maze = self.do_not_perfect(maze)
        self.get_map(maze)

    @classmethod
    def do_not_perfect(cls, maze: list[list[int]] = []) -> list[list[int]]:
        # dell all deadends

        for y in range(0, len(maze)):
            for x in range(0, len(maze[0])):
                # check for dead end - there is 3 wall
                v = maze[y][x]
                if (v & 0xf) == 0xf:   # skeep pattern, entry, exit
                    continue
                v = v & 3
                if y == 0:
                    v = v | 1
                if x == 0:
                    v = v | 8
                elif (maze[y][x-1] & 2):
                    v = v | 8
                if y == (len(maze)-1):
                    v = v | 4
                elif (maze[y+1][x] & 1):
                    v = v | 4
                if x == (len(maze[0])-1):
                    v = v | 2
                w = v
                if len([(1 << i) for i in range(4) if (v >> i) & 1]) == 3:
                    # dead end found
                    # print(f"dead end x={x}, y={y}, w={w}")
                    # Trying to delete wall
                    # At first try to find walls that could be removed
                    if w & 1:   # top
                        if y == 0:
                            w = w & 0xe  # e  1110
                        elif (maze[y-1][x] & 0xf) == 0xf:     # pattern
                            w = w & 0xe
                    if w & 2:   # reight
                        if x == (len(maze[0])-1):
                            w = w & 13   # d  1101
                        elif (maze[y][x+1] & 0xf) == 0xf:     # pattern
                            w = w & 13
                    if w & 4:   # bottom
                        if y == (len(maze)-1):
                            w = w & 11   # b  1011
                        elif (maze[y+1][x] & 0xf) == 0xf:     # pattern
                            w = w & 11
                    if w & 8:   # left
                        if x == 0:
                            w = w & 7   # 7  0111
                        elif (maze[y][x-1] & 0xf) == 0xf:     # pattern
                            w = w & 7
                    if (w == 0):     # walls can`t be removed
                        continue
                    chosen_wall = random.choice([(1 << i) for i in range(4)
                                                 if (w >> i) & 1])
                    #  print("wall:", chosen_wall)
                    match chosen_wall:
                        case 1:
                            # 1 - (xxx1) Top wall (North)
                            maze[y][x] = maze[y][x] & 0xfffe
                            maze[y-1][x] = maze[y-1][x] & 0xfffb
                            # print("del", chosen_wall, ":", (x, y))
                            continue
                        case 2:
                            # 2 - (xx1x) Right (East)
                            maze[y][x] = maze[y][x] & 0xfffd
                            maze[y][x+1] = maze[y][x+1] & 0xfff7
                            # print("del", chosen_wall, ":", (x, y))
                            continue
                        case 4:
                            # 4 - (x1xx) Bottom (South)
                            maze[y+1][x] = maze[y+1][x] & 0xfffe
                            maze[y][x] = maze[y][x] & 0xfffb
                            # print("del", chosen_wall, ":", (x, y))
                            continue
                        case 8:
                            # 8 - (1xxx) Left
                            maze[y][x-1] = maze[y][x-1] & 0xfffd
                            maze[y][x] = maze[y][x] & 0xfff7
                            # print("del", chosen_wall, ":", (x, y))
                            continue

        return maze

    def print(self, maze_: list[list[int]] = []) -> None:

        print("*"*30)
        if len(maze_) <= 0:
            for y in range(0, self.rows):
                l_ = []
                for x in range(0, self.cols):
                    l_.append(self.world_map.get((x, y), 0))
                maze_.append(l_)
        # else:
        #     print("Maze size:", len(maze_))

        if len(maze_) > 0:
            print("Maze size (x,y):", (len(maze_[0]), len(maze_)))
            print("    ", end="")
            for x in range(0, len(maze_[0])):
                print(f"{x % 10} ", end="")
            print()
        for row_ in range(0, len(maze_)):
            print(f"{row_:2}", "{", end="")
            for v_ in maze_[row_]:
                v_ = v_ & 15
                if v_ == 15:
                    print("🞓 ", end="")  # ▢ ▧ █
                elif v_ == 0:
                    print("∘ ", end="")
                elif v_ == 1:
                    print("🭶 ", end="")  # ‾
                elif v_ == 13:  # oxD = 13 = 1101
                    print("ᑕ ", end="")
                elif v_ == 8:
                    print("▏ ", end="")  # 🭰[ ▏
                elif v_ == 2:
                    print("▕ ", end="")  # ] ▕ 🭵 ▕
                elif v_ == 4:
                    print("🭻 ", end="")  # _
                elif v_ == 1+4:
                    print("🮀 ", end="")  # =〓⚌
                elif v_ == 2+8:
                    print("⣿ ", end="")  # Ⅱ ⏸ ᱿ ║
                elif v_ == 8 + 4:
                    print("🭼 ", end="")  # ᒪ ᄂ ∟ ⌞
                elif v_ == 3:
                    print("🭾 ", end="")  # ᄀ ⌝
                elif v_ == 2 + 4:
                    print("🭿 ", end="")  # ᒧ ⌟
                elif v_ == 1 + 8:
                    print("🭽 ", end="")  # ᒥ ⌜
                elif v_ == 2+4+8:
                    print("ᑌ ", end="")
                elif v_ == 1+2+8:
                    print("ᑎ ", end="")
                elif v_ == 1+2+4:
                    print("ᑐ ", end="")
                else:
                    print(f"{v_:1}", end="")
            print("}")
        # for row_ in maze_:
        #     print("[",end=" ")
        #     for v_ in row_:
        #         print(f"{v_:3}",end=" ")
        #     print("]")
        # 	  ⠿⠼⠯⠇⠸⠹

        print("*"*30)

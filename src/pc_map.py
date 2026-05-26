import pygame as pg
from collections import deque

_ = False
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]


class Map:
    def __init__(self, game):
        self.game = game
#        self.mini_map = mini_map
        self.world_map = {}
        self.rows = 1
        self.cols = 1
        self.cell_size = 35
        self.wall_thickness = 4
        self.step = self.cell_size + self.wall_thickness
        self.top = self.step
        self.get_map()

    def get_map(self):
        pass
        # for j, row in enumerate(self.mini_map):
        #     for i, value in enumerate(row):
        #         if value:
        #             self.world_map[(i, j)] = value

    def get_map_form_file(self, file_name: str):
        self.world_map = {}
        y: int = 0
        with open(file_name, "r", encoding="utf-8") as f:
            for line in f:
                l_ = line.strip()
                if y == 0:
                    self.cols = len(l_)
                if len(l_) < self.cols:
                    self.rows = y
                    return
                for x in range(0, len(l_)):
                    v = int(l_[x], 16)
                    if v > 0:
                        self.world_map[(x, y)] = v
                y += 1

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

    def draw(self):
        pg.draw.rect(self.game.screen, 'green', (0, self.top,
                     self.wall_thickness,
                     self.rows * self.step
                     + self.wall_thickness), 0)
        pg.draw.rect(self.game.screen, 'green',
                     (0, self.rows * self.step
                      + self.top,
                      self.cols * self.step,
                      self.wall_thickness), 0)

        for pos in self.world_map:
            w = self.world_map[pos] & 15
            if w == 15:  # call is part of 42 pattern (isolated cell)
                pg.draw.rect(self.game.screen, 'white',
                             (pos[0] * self.step
                              + self.wall_thickness,
                              pos[1] * self.step
                              + self.top + self.wall_thickness,
                              self.cell_size,
                              self.cell_size), 0)
            if (w & 2) == 2:
                pg.draw.rect(self.game.screen, 'green',
                             ((pos[0] + 1) * self.step,
                              pos[1] * self.step
                              + self.top,
                              self.wall_thickness,
                              self.cell_size + self.wall_thickness * 2), 0)
            if (w & 1) == 1:
                pg.draw.rect(self.game.screen, 'green',
                             (pos[0] * self.step,
                              pos[1] * self.step
                              + self.top,
                              self.cell_size + self.wall_thickness * 2,
                              self.wall_thickness), 0)

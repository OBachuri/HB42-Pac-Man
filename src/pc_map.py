import pygame as pg

_ = False
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 4, _, _, _, 4, _, _, _, _, _, _, 1],
    [1, 1, 1, 3, 1, 3, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 3, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 4, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, 3, 4, _, 4, 3, _, 1],
    [1, _, _, 5, _, _, _, _, _, _, 3, _, 3, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 4, _, _, _, _, _, _, 4, _, _, 4, _, _, _, 1],
    [1, 1, 3, 3, _, _, 3, 3, 1, 3, 3, 1, 3, 1, 1, 1],
    [1, 1, 1, 3, _, _, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 4, _, _, 4, 3, 3, 3, 3, 3, 3, 3, 3, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, 5, _, _, _, 5, _, _, _, 5, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]


class Map:
    def __init__(self, game):
        self.game = game
#        self.mini_map = mini_map
        self.world_map = {}
        self.rows = 1
        self.cols = 1
        self.cell_size = 30
        self.wall_thickness = 4
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
                    self.world_map[(x, y)] = int(l_[x], 16)
                y += 1

    def draw(self):
        pg.draw.rect(self.game.screen, 'green', (0, 0,
                     self.wall_thickness,
                     self.rows*(self.cell_size + self.wall_thickness)
                     + self.wall_thickness), 0)
        pg.draw.rect(self.game.screen, 'green',
                     (0, self.rows*(self.cell_size + self.wall_thickness),
                      self.cols*(self.cell_size + self.wall_thickness),
                      self.wall_thickness), 0)

        [pg.draw.rect(self.game.screen, 'white',
                      (pos[0] * (self.cell_size+self.wall_thickness),
                       pos[1] * (self.cell_size+self.wall_thickness),
                       self.cell_size + self.wall_thickness * 2,
                       self.cell_size + self.wall_thickness * 2), 0)
         for pos in self.world_map if self.world_map[pos] & 15 == 15]

        [pg.draw.rect(self.game.screen, 'green',
                      (pos[0] * (self.cell_size+self.wall_thickness),
                       pos[1] * (self.cell_size+self.wall_thickness),
                       self.cell_size + self.wall_thickness * 2,
                       self.wall_thickness), 0)
         for pos in self.world_map if self.world_map[pos] & 1 == 1]
        [pg.draw.rect(self.game.screen, 'green',
                      ((pos[0]+1) * (self.cell_size+self.wall_thickness),
                       pos[1] * (self.cell_size+self.wall_thickness),
                       self.wall_thickness,
                       self.cell_size + self.wall_thickness * 2), 0)
         for pos in self.world_map if self.world_map[pos] & 2 == 2]

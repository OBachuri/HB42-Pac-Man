import pygame as pg
from src.pc_npc import GhostMode

class PC_Artifacts():
    """
    Artifacts = Pellet or  PowerPellet

    Pellet = Dot = Pacgums
    PowerPellet = Super-pacgums = Energizer
    """
    def __init__(self, game, point=(0, 0), points=10, color=(200, 200, 200)):
        self.game = game
        self.x, self.y = point
        self.size = 2  # radius
        self.color = color
        self.points = points  # score add
        self.frames = []

    def draw(self):
        x = (self.x * self.game.map.step
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness)

        y = (self.y * (self.game.map.step)
             + self.game.map.cell_size / 2
             + self.game.map.wall_thickness
             + self.game.map.top)

        if len(self.frames) == 0: 
            pg.draw.circle(self.game.screen,
                       self.color,
                       (x, y), self.size)
            

    def event(self):
        self.game.score += self.points
        self.points = 0
        self.color = (255, 255, 255)
        self.draw()
        # self.game.player.dx = max(0, self.game.player.dx - 0.1)
        # self.game.player.dy = max(0, self.game.player.dy - 0.1)
        self.game.artifacts.remove(self)

    def update(self):
        x = int(round(self.game.player.x, 0))
        y = int(round(self.game.player.y, 0))
        if (x, y) == (self.x, self.y):
            if ((self.x - self.game.player.x)**2
                + (self.y
                   - self.game.player.y)**2) < (self.size
                                                + self.game.player.size)**2:
                self.event()


class PowerPellet(PC_Artifacts):
    # PowerPellet = Super-pacgums = Energizer
    def __init__(self, game, point=(0, 0), points=50, color=(220, 250, 220)):
        super().__init__(game, point, points, color)
        self.size = 6  # radius

    def event(self):
        super().event()
        self.game.player.dx = max(0, self.game.player.dx - 3)
        self.game.player.dy = max(0, self.game.player.dy - 3)
        for n in self.game.npcs:
            n.mode = GhostMode.SCATTER


class Pellet(PC_Artifacts):
    # Pellet = Pacgums = Dots
    def __init__(self, game, point=(0, 0), points=10, color=(220, 220, 250)):
        super().__init__(game, point, points, color)

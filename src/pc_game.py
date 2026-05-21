from src.pc_map import Map
from src.pc_player import Player
import pygame as pg
import sys

FPS = 60


class Game:
    def __init__(self):
        pg.init()
        # pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode((800, 800))
        # pg.display.set_caption("Pac-Man 42")
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        pg.font.init()
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)

    def update(self):
        self.player.update()
        # self.raycasting.update()
        # self.object_handler.update()
        # self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption('Pac-man  42 '
                               f'(fps:{self.clock.get_fps(): 6.1f})')

    def draw(self):
        self.screen.fill('black')
        # self.object_renderer.draw()
        # self.weapon.draw()
        self.map.draw()
        self.player.draw()

        self.screen.blit(self.font.render(
            'Move:  W A S D, Stop: Space, Exit: Esc', False, (10, 10, 200)),
            (10, 10 + (self.map.rows)
             * (self.map.cell_size + self.map.wall_thickness)))

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                         and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            # self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

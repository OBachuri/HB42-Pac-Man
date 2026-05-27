from src.pc_map import Map
from src.pc_player import Player
from src.pc_npc import NPC
from src.pc_artifact import PC_Artifacts
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
        self.game_time = 110   # sec
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        self.score = 0
        self.gost_edible = 7  # sec - frightened time
        pg.time.set_timer(self.global_event, 40)
        pg.font.init()
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.npcs: list[NPC] = []
        self.artifacts: list[PC_Artifacts] = []
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        #  self.npcs = [NPC(self), NPC(self), NPC(self), NPC(self)]

    def update(self):
        self.player.update()
        for npc in self.npcs:
            npc.update()
        for pellet in self.artifacts:
            pellet.update()
        # self.raycasting.update()
        # self.object_handler.update()
        # self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        self.game_time -= self.delta_time / 1000
        pg.display.set_caption('Pac-man  42 '
                               f'(fps:{self.clock.get_fps(): 6.1f})')

    def draw(self):
        self.screen.fill('black')
        # self.object_renderer.draw()
        # self.weapon.draw()
        self.map.draw()
        for pellet in self.artifacts:
            pellet.draw()
        self.player.draw()
        for npc in self.npcs:
            npc.draw()

        self.screen.blit(self.font.render(
            'Move:  W A S D, Stop: Space, Exit: Esc', False, (10, 10, 200)),
            (10, 10 + self.map.top + (self.map.rows)
             * (self.map.step)))

        self.screen.blit(self.font.render(
            f'Time: {self.game_time: 4.1f},    '
            f'Lives: {self.player.lives},    '
            f'Level: 1,   Score: {self.score}',
            False, (200, 200, 200)),
            (10, 8))

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

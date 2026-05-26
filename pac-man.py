import pygame as pg
# from typing import cast
from pydantic import ValidationError
import sys
# import os

from mazegen import CMazeParams, MazeGenerator, CAlg
# from src.pc_map import Map
# from src.pc_player import Player
from src.pc_game import Game
from src.pc_npc import NPC, RedGhosts

# RES = WIDTH, HEIGHT = 1000, 800
# FPS = 0


def main() -> int:
    try:
        c_mz_param = CMazeParams(width=25,
                                 height=20,
                                 entry=(0, 0),
                                 exit=(0, 1),
                                 output_file="maze_txt.txt",
                                 perfect=False,
                                 insert_42=True,
                                 algorithm=CAlg.DFS
                                 )
    except ValidationError as e:
        # for err in e.errors():
        #     print(err["msg"])
        print(e, file=sys.stderr)
        sys.exit(1)

    print("Maze config:", c_mz_param.print())
    maze_ = MazeGenerator.generate(c_mz_param)
    MazeGenerator.write_to_file(maze_, c_mz_param, [])
    print(f"The maze saved to file '{c_mz_param.output_file}'")

    game = Game()
    # print(game.map.world_map)
    # print("*"*30)
    game.map.get_map_form_file(c_mz_param.output_file)
    game.player.teleport()
    game.npcs.append(RedGhosts(game))
    game.npcs.append(NPC(game, (game.map.cols - 1, 0),
                         (240, 24, 140), "Pink gost (Speedy)"))
    game.npcs.append(NPC(game,
                         (game.map.cols - 1, game.map.rows - 1),
                         (100, 250, 250), "Cyan gost (Inky, Bashful)"))
    game.npcs.append(NPC(game,
                         (0, game.map.rows - 1),
                         (250, 120, 10), "Orange gost (Clyde, Pockey)"))
    game.npcs[0].goal = (game.player.x, game.player.y)
    game.npcs[1].goal = (game.player.x, game.player.y)
    game.npcs[2].goal = (game.player.x, game.player.y)
    game.npcs[3].goal = (game.player.x, game.player.y)

    # print(game.map.world_map)
    game.screen = pg.display.set_mode(
        (max(game.map.cols*game.map.step
         + game.map.wall_thickness, 500),
         (game.map.rows + 3)*(game.map.step)))
    # print(dir(pg.draw))
    game.run()

    return (0)


if __name__ == "__main__":
    main()

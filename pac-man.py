import pygame as pg
# from typing import cast
from pydantic import ValidationError
import sys
import random
# import os


# from src.pc_map import Map
# from src.pc_player import Player
from src.pc_game import Game
from src.pc_npc import NPC, RedGhosts
from src.pc_artifact import PowerPellet, Pellet

# RES = WIDTH, HEIGHT = 1000, 800
# FPS = 0


def main() -> int:

    pacgum = 1421

    our_mazgen = False
    maze_ = []

    # try our maze generator
    # try:
    #     from mazegen import CMazeParams, MazeGenerator, CAlg
    #     our_mazgen = True
    # except Exception as err_msg:
    #     our_mazgen = False
    #     # print("Error with mazegen library connection:", err_msg)
    #     # sys.exit(1)

    # try shcool maze generator
    if not our_mazgen:
        try:
            print("*"*40)
            from mazegenerator.mazegenerator import MazeGenerator
            # from mazegenerator import MazeGenerator
        except Exception as err_msg:
            print("Error with mazegen library connection:", err_msg)
            sys.exit(1)

        print("Maze generation - start  ...")
        maze_ = MazeGenerator(size=(14, 14), perfect=False).maze
        print("Maze generation - end")

    else:

        try:
            c_mz_param = CMazeParams(width=20,
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

    
    game.map.print(maze_)

    
    maze_ = game.map.do_not_prefect(maze_)

    # game.map.get_map_form_file(c_mz_param.output_file)
    game.map.get_map(maze_)
    game.map.print()

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

    #  Add PowerPellet and Pellet
    game.artifacts.append(PowerPellet(game, (0, 0)))
    game.artifacts.append(PowerPellet(game, (game.map.cols - 1, 0)))
    game.artifacts.append(PowerPellet(game,
                                      (game.map.cols - 1, game.map.rows - 1)))
    game.artifacts.append(PowerPellet(game, (0, game.map.rows - 1)))

    place_set = {(x, y) for x in range(0, game.map.cols)
                 for y in range(0, game.map.rows)
                 if (game.map.world_map.get((x, y), 0) & 15 != 15)}

    for a_ in game.artifacts:
        place_set.remove((a_.x, a_.y))

    if pacgum <= 0:
        for s_ in place_set:
            game.artifacts.append(Pellet(game, s_))
    else:
        for p in range(0, pacgum):
            if (len(place_set) < 1):
                print(f"All Pellets can't be placed ({p+1} from {pacgum}).")
                break
            x, y = random.choice(tuple(place_set))
            game.artifacts.append(Pellet(game, (x, y)))
            place_set.remove((x, y))

    # print(game.map.world_map)
    game.screen = pg.display.set_mode(
        (max(game.map.cols*game.map.step
         + game.map.wall_thickness, 550),
         (game.map.rows + 3)*(game.map.step)))
    # print(dir(pg.draw))
    game.run()

    return (0)


if __name__ == "__main__":
    main()

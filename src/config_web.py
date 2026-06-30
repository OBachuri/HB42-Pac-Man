from typing import Any

from pc_artifact import BonusFruitType


class LevelWeb:
    def __init__(self, data: dict[str, Any] = {}) -> None:
        self.number: int = 1
        try:
            n = int(data.get("number", 1))
            if n < 0:
                raise ValueError("Number of level must be positive integer")
            self.number = n
        except Exception as ex:
            print("Error in config in level number =",
                  data.get("number", 1), ":", ex)

        self.map_filename: str = ""
        try:
            str_ = str(data.get("map_filename", ""))
            self.map_filename = str_
        except Exception as ex:
            print(f"Error in config for level {self.number} "
                  "- wrong map file name",
                  data.get("map_filename", ""), ":", ex)

        self.remove_deadends: bool = data.get("remove_deadends", True)
        self.width: int = max(data.get("width", 14), 3)
        self.height: int = max(data.get("height", 10), 3)
        self.seed: int = data.get("seed", 0)
        self.pacgum: int = data.get("pacgum", 0)
        self.level_max_time: int = data.get("level_max_time", 90)
        self.speed_factor_player: float = data.get(
            "speed_factor_player", 0.01)
        self.speed_factor_ghost: float = data.get(
            "speed_factor_ghost", 0.02)
        self.max_player_acceleration: int = data.get(
            "max_player_acceleration", 5)
        self.points_per_bonus_fruit: int = data.get(
            "points_per_bonus_fruit", 100)
        try:
            f_nane = str(data.get("bonus_fruit_type", "cherry"))
            fruit = BonusFruitType[f_nane.upper()]
        except KeyError:
            fruit = BonusFruitType.CHERRY
            print("Can't find fruit: ", f_nane, "!")
        self.bonus_fruit_type: BonusFruitType = fruit
        self.fullscreen_mode: bool = False
        try:
            self.fullscreen_mode = bool(data.get("fullscreen_mode", False))
        except Exception as ex:
            print("Error: Wrong value of fullscreen_mode - ", ex)

    @property
    def size(self) -> tuple[int, int]:
        return (self.width, self.height)

    def print(self) -> None:
        print("--Level:")
        print("Number:", self.number)
        print("Width:", self.width)
        print("Height:", self.height)
        print("Map File:", self.map_filename)
        print("Seed:", self.seed)
        print("Remove deadends:", self.remove_deadends)
        print("Time max:", self.level_max_time, "s")


class ConfigWeb:
    def __init__(self, cfg_data: dict[str, Any] = {}) -> None:
        self.highscores_filename: str = cfg_data.get(
            "highscores_filename", "highscores.json")
        self.lives: int = cfg_data.get("lives", 3)
        self.points_per_pacgum: int = cfg_data.get("points_per_pacgum", 10)
        self.points_per_super_pacgum: int = cfg_data.get(
            "points_per_super_pacgum", 50)
        self.points_per_ghost: int = cfg_data.get("points_per_ghost", 200)
        self.seed: int = cfg_data.get("seed", 0)
        self.cheat: bool = cfg_data.get("cheat", False)

        try:
            levels: list[LevelWeb] = [LevelWeb(level_data)
                                      for level_data
                                      in cfg_data.get("levels", [])]
            min_level = 0
            min_level = min({l_.number for l_ in levels})
            if min_level != 1:
                print("Error: in config must be Level number 1!")
                levels.append(LevelWeb())
        except Exception as ex:
            print("Error in config for levels:", ex)
            levels = []

        self.levels: list[LevelWeb] = levels if levels else [LevelWeb()]

    def print(self) -> None:
        print("--Config:")
        print("Seed:", self.seed)
        print("Cheat:", self.cheat)
        print("Levels: ", len(self.levels))
        for l_ in self.levels:
            l_.print()

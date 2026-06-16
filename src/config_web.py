from typing import Any


class LevelWeb:
    def __init__(self, data: dict[str, Any] = {}) -> None:
        self.map_filename: str = data.get("map_filename", "")
        self.number: int = data.get("number", 1)
        self.rmv_deadends: bool = data.get("remove_deadends", False)
        self.width: int = data.get("width", 14)
        self.height: int = data.get("height", 12)
        self.seed: int = data.get("seed", 0)
        self.pacgum: int = data.get("pacgum", 42)
        self.level_max_time: int = data.get("level_max_time", 90)
        self.speed_factor_player: float = data.get(
            "speed_factor_player", 0.01)
        self.speed_factor_ghost: float = data.get(
            "speed_factor_ghost", 0.02)


class ConfigWeb:
    def __init__(self, cfg_data: dict[str, Any] = {}) -> None:
        self.highscores_filename: str = cfg_data.get(
            "highscores_filename", "highscores.json")
        self.lives: int = cfg_data.get("lives", 3)
        self.points_per_pacgum: int = cfg_data.get("points_per_pacgum", 10)
        self.points_per_super_pacgum: int = cfg_data.get(
            "points_per_super_pacgum", 50)
        self.points_per_ghost: int = cfg_data.get("points_per_ghost", 200)
        self.seed: int = cfg_data.get("seed", 42)
        self.cheat: bool = cfg_data.get("cheat", False)

        levels: list[LevelWeb] = [LevelWeb(level_data)
                                  for level_data
                                  in cfg_data.get("levels", [])]

        self.levels: list[LevelWeb] = levels if levels else [LevelWeb()]

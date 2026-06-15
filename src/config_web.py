from typing import Any


class LevelWeb:
    def __init__(self, data: dict[str, Any] = {}) -> None:
        self.map_filename: str = data.setdefault("map_filename", "")
        self.number: int = data.setdefault("number", 1)
        self.rmv_deadends: bool = data.setdefault("remove_deadends", False)
        self.width: int = data.setdefault("width", 14)
        self.height: int = data.setdefault("height", 12)
        self.seed: int = data.setdefault("seed", 0)
        self.pacgum: int = data.setdefault("pacgum", 42)
        self.level_max_time: int = data.setdefault("level_max_time", 90)
        self.speed_factor_player: float = data.setdefault("speed_factor_player", 0.01)
        self.speed_factor_ghost: float = data.setdefault("speed_factor_ghost", 0.02)


class ConfigWeb:
    def __init__(self, cfg_data: dict[str, Any] = {}) -> None:
        self.highscores_filename: str = cfg_data.setdefault("highscores_filename", "highscores.json")
        self.lives: int = cfg_data.setdefault("lives", 3)
        self.points_per_pacgum: int = cfg_data.setdefault("points_per_pacgum", 10)
        self.points_per_super_pacgum: int = cfg_data.setdefault("points_per_super_pacgum", 50)
        self.points_per_ghost: int = cfg_data.setdefault("points_per_ghost", 200)
        self.seed: int = cfg_data.setdefault("seed", 42)
        self.cheat: bool = cfg_data.setdefault("cheat", False)

        levels: list[LevelWeb] = [LevelWeb(level_data) for level_data in cfg_data.setdefault("levels", [])]
        self.levels: list[LevelWeb] = levels if levels else [LevelWeb()]

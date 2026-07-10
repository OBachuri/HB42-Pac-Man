import json
import os
import sys
import pygame as pg
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from config import Config
    from config_web import ConfigWeb


class HighscoresHandler:
    """Read and persist Top 10 highscores for desktop and web platforms."""

    @staticmethod
    def get_highscores(config: "Config | ConfigWeb") -> list[dict[str, int]]:
        """Load highscores from storage and return them sorted descending.

        Args:
            config (Config | ConfigWeb): Runtime config with highscores file.

        Returns:
            list[dict[str, int]]: Sorted highscore entries, or empty list on
            read/format errors.
        """

        highscores: list[dict[str, int]] = []
        path = config.highscores_filename
        if sys.platform == "emscripten":
            save_dir = pg.system.get_pref_path("42hr.fr", "PacMan")
            path = os.path.join(save_dir, config.highscores_filename)
        try:
            with open(path) as f:
                highscores = json.load(f)
                if not isinstance(highscores, list):
                    return []
                highscores.sort(key=lambda d: list(
                    d.values())[0], reverse=True)
        except Exception:
            pass
        return highscores

    @classmethod
    def store_highscores(cls, config: "Config | ConfigWeb",
                         name: str, score: int) -> None:
        """Insert a new score, keep top 10 entries, and write to storage.

        Args:
            config (Config | ConfigWeb): Runtime config with highscores file.
            name (str): Player name to store.
            score (int): Score value associated with the player.
        """

        highscores = cls.get_highscores(config)
        highscores.insert(0, {name: score})
        highscores.sort(key=lambda d: list(d.values())[0], reverse=True)
        highscores = highscores[:10]

        path = config.highscores_filename
        if sys.platform == "emscripten":
            save_dir = pg.system.get_pref_path("42hr.fr", "PacMan")
            path = os.path.join(save_dir, config.highscores_filename)
        try:
            with open(path, "w") as f:
                json.dump(highscores, f, indent=2)
        except Exception as e:
            print("\nError: Could not store highscores.")
            print(e)

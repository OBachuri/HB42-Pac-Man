import json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from config import Config


class HighscoresHandler:
    @staticmethod
    def get_highscores(config: "Config") -> list[dict[str, int]]:
        highscores: list[dict[str, int]] = []
        try:
            with open(config.highscores_filename) as f:
                highscores = json.load(f)
                if not isinstance(highscores, list):
                    return []
                highscores.sort(key=lambda d: list(d.values())[0], reverse=True)
        except Exception:
            pass
        return highscores

    @classmethod
    def store_highscores(cls, config: "Config", name: str, score: int) -> None:
        highscores = cls.get_highscores(config)
        highscores.insert(0, {name: score})
        highscores.sort(key=lambda d: list(d.values())[0], reverse=True)
        highscores = highscores[:10]

        try:
            with open(config.highscores_filename, "w") as f:
                json.dump(highscores, f, indent=2)
        except Exception as e:
            print("\nError: Could not store highscores.")
            print(e)

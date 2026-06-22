import json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from config import Config


class HighscoresHandler:
    highscores: list[dict[str, int]] = []

    @classmethod
    def get_highscores(cls, config: "Config") -> list[dict[str, int]]:
        try:
            with open(config.highscores_filename) as f:
                cls.highscores = json.load(f)
        except Exception:
            pass
        return cls.highscores

    @classmethod
    def store_highscores(cls, config: "Config", score: dict[str, int]) -> None:
        highscores = cls.highscores
        highscores.append(score)
        sorted_scores = sorted(highscores, key=lambda d: list(d.values())[0], reverse=True)
        cls.highscores = sorted_scores[:5]

        try:
            with open(config.highscores_filename, "w") as f:
                f.write(json.dumps(cls.highscores, indent=2))
        except Exception as e:
            print("\nERROR!!! Could not store highscores!")
            print(e)

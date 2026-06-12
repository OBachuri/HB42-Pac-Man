import json
from typing import Any
from src.config import Config


class Parser:
    @staticmethod
    def _get_config_data(path: str) -> dict[str, Any]:
        result: dict[str, Any] = {}
        try:
            with open(path) as f:
                raw_text = f.readlines()
                clean_json = [line for line in raw_text
                              if not line.strip().startswith("#")]
                result = json.loads("".join(clean_json))
                if not result:
                    print("Could not extract config")
        except json.JSONDecodeError as e:
            print("Got JSON decoding error:", e)
        except FileNotFoundError:
            print(f"Config file not found: {path}")
        return result

    @classmethod
    def get_config(cls, path: str) -> Config:
        cfg_data = cls._get_config_data(path)

        if not cfg_data:
            print("Using default demo config settings")

        return Config(**cfg_data)

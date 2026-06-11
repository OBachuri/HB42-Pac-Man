import sys
import json
from typing import Dict, Any
from pydantic import ValidationError
from src.config import Config


class Parser:
    @classmethod
    def _get_config_data(cls, path: str) -> Dict[str, Any]:
        try:
            with open(path) as f:
                raw_text = f.readlines()
                clean_json = [line for line in raw_text
                            if not line.strip().startswith("#")]
                return json.loads("".join(clean_json))
        except json.JSONDecodeError as e:
            print("\nGot JSON decoding error:", e)
        except FileNotFoundError as e:
            print(f"\nConfig file not found: {path}")
        sys.exit(1)
    
    @classmethod
    def get_config(cls, path: str) -> Config:
        cfg_data = cls._get_config_data(path)

        try:
            return Config.model_validate(cfg_data)
        except ValidationError as e:
            print(f"\nGot an error:", e)
            sys.exit(1)

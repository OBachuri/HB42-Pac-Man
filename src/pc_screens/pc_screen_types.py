from enum import Enum


class ScreenTypes(Enum):
    """Identifiers for application screens used in navigation flow."""

    MAIN_MENU = "main_menu"
    GAME = "game"
    INSTRUCTIONS = "instructions"
    HIGH_SCORES = "high_scores"
    END_OF_GAME = "end_of_game"
    ERROR = "error"

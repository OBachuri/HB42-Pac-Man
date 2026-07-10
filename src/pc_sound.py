import os
from enum import Enum
from pygame import mixer as mx


class SoundType(Enum):
    """Identifiers for grouped in-game sound effects."""

    EATEN = 1    # death
    REBORN = 2
    DISAPPEAR = 3
    TICK = 9


class Sound:
    """Thin wrapper around pygame mixer sound loading and playback."""

    def __init__(self, file_path: str) -> None:
        """Create a sound object from a file if it exists and is readable.

        Args:
            file_path (str): Path to a sound file.
        """

        self._path: str = self._file_path_test(file_path)
        self._sound: mx.Sound | None = None
        if len(self._path) > 0:
            try:
                mx_sound = mx.Sound(self._path)
                self._sound = mx_sound
            except Exception as ex:
                print("Can't read sound from file:", file_path, ex)

    def _file_path_test(self, file_path: str) -> str:
        """Validate file path existence.

        Args:
            file_path (str): Candidate file path.

        Returns:
            str: Original path if it exists, otherwise an empty string.
        """

        if os.path.exists(file_path):
            return (file_path)
        else:
            return ("")

    def play(self, loops: int = 0) -> None:
        """Play the loaded sound.

        Args:
            loops (int, optional): Number of extra repeats (0 = play once).
        """

        if self._sound:
            try:
                mx.Sound.play(self._sound, loops=loops)
            except Exception as ex:
                print("Error with sound play:", ex)

    def stop(self) -> None:
        """Stop playback of the loaded sound."""

        if self._sound:
            try:
                mx.Sound.stop(self._sound)
            except Exception as ex:
                print("Error with sound play:", ex)

    @staticmethod
    def read_sounds_from_files(file_path: str, sound_type: SoundType,
                               sounds: dict[SoundType, list["Sound"]] = {}
                               ) -> dict[SoundType, list["Sound"]]:
        """Load sound files for a sound type and append them to a registry.

        Args:
            file_path (str): Directory or pattern source for sound files.
            sound_type (SoundType): Sound category key.
            sounds (dict[SoundType, list[Sound]], optional): Existing sound
                registry to extend.

        Returns:
            dict[SoundType, list[Sound]]: Updated sound registry.
        """

        path_ = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                file_path,
            )
        if os.path.exists(path_):
            files = sorted(
                f for f in os.listdir(path_)
                if f.lower().endswith(
                    (".ogg")
                )
            )
            if len(sounds.get(sound_type, [])) == 0:
                sounds[sound_type] = []

            for filename in files:
                sound_ = Sound(path_+filename)
                sounds[sound_type].append(sound_)

            if not sounds[sound_type]:
                print(f"No sound files found in {path_}.")
        else:
            print(f"Can't find sound files in {file_path}"
                  f"for {sound_type.name}.")
        return (sounds)

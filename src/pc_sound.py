import os
from enum import Enum
from pygame import mixer as mx


class SoundType(Enum):
    EATEN = 1,   # death
    REBORN = 2


class Sound:
    def __init__(self, file_path: str) -> None:
        self._path: str = self._file_path_test(file_path)
        self._sound: mx.Sound | None = None
        if len(self._path) > 0:
            try:
                mx_sound = mx.Sound(self._path)
                self._sound = mx_sound
            except Exception as ex:
                print("Can't read sound from file:", file_path, ex)

    def _file_path_test(self, file_path: str) -> str:
        if os.path.exists(file_path):
            return (file_path)
        else:
            return ("")

    def play(self, loops: int = 0) -> None:
        if self._sound:
            mx.Sound.play(self._sound, loops=loops)

    def stop(self) -> None:
        if self._sound:
            mx.Sound.stop(self._sound)

    @staticmethod
    def read_sounds_from_files(file_path: str, sound_type: SoundType,
                               sounds: dict[SoundType, list["Sound"]] = {}
                               ) -> dict[SoundType, list["Sound"]]:
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

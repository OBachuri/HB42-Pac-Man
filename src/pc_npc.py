from __future__ import annotations

import pygame as pg
import random
from collections.abc import Sequence
# from enum import Enum
from pc_entity import Entity, FrameType, GhostMode
from pc_constants import FPS
from pc_sound import SoundType, Sound

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pc_game import Game


class NPC(Entity):
    """Ghost entity with AI modes, collision events, and respawn behavior."""

    def __init__(self, game: Game,
                 point: tuple[int | float, int | float] = (0, 0),
                 color: tuple[int, int, int] = (100, 100, 100),
                 name: str = "Ghost", size: int = 11, points: int = 200):
        """Initialize ghost state, movement traits, and score value.

        Args:
            game (Game): Active game context.
            point (tuple[int | float, int | float], optional): Spawn position.
            color (tuple[int, int, int], optional): Ghost render color.
            name (str, optional): Ghost name.
            size (int, optional): Collision/render size factor.
            points (int, optional): Base score awarded when eaten.
        """

        super().__init__(game, point=point, color=color, name=name, size=size)
        self.speed_factor: float = 0.02
        self.points = points  # score add

        # for mypy test - it can't check type from Entity
        self.dx: int = 0
        self.dy: int = 0

        self.goal: pg.Vector2 | None = None
        self.x: float | int = 0
        self.y: float | int = 0
        self.x, self.y = point
        self.angle: float | int = 0
        self.animation_timer: float = 0
        self.event_timer: float = 0
        self.sounds: dict[SoundType, list[Sound]] = {}
        self.sound_index: int = 0
        # end of block for mypy

        self.start_chase_if_near: int = 4
        self.mode: GhostMode = GhostMode.CHASE

        self.read_frames_from_file("inc/img/frightened/", FrameType.FRIGHTENED)
        self.read_frames_from_file("inc/img/end_of_frightened/",
                                   FrameType.END_OF_FRIGHTENED)
        self.read_frames_from_file("inc/img/ghost/death/", FrameType.DEATH)
        self.read_frames_from_file("inc/img/ghost/eyes/down/", FrameType.DOWN)
        self.read_frames_from_file("inc/img/ghost/eyes/up/", FrameType.UP)
        self.read_frames_from_file("inc/img/ghost/eyes/left/", FrameType.LEFT)
        self.read_frames_from_file("inc/img/ghost/eyes/right/",
                                   FrameType.RIGHT)
        self.read_frames_from_file("inc/img/ghost/eyes/stay/", FrameType.DEAD)

        self.alive: bool = True
        self.visible: bool = True
        self.freeze: bool = False

        self.old_keys: Sequence[bool] = pg.key.get_pressed()

        self.sound_init()

        # print("Created:",
        #       self.name, "x:", self.x, ", y:",
        #       self.y, ", vis:", self.visible,
        #       ", goal:", self.goal)

    def get_speed_factor(self) -> float:
        """Return effective movement speed based on current ghost mode.

        Returns:
            float: Mode-adjusted speed factor.
        """

        speed_factor = min(self.speed_factor, 0.5)
        if self.mode == GhostMode.SPAWN:
            speed_factor = max(0.05, speed_factor)
        if self.mode == GhostMode.FRIGHTENED:
            speed_factor = min(0.03, speed_factor)
        return (speed_factor)

    def find_goal(self) -> None:
        """Compute the current navigation target for ghost pathing."""

        speed_factor = self.get_speed_factor()
        cur_x = round(self.x)
        cur_y = round(self.y)

        if self.mode == GhostMode.SCATTER:
            if (self.goal is None
               or self.goal.distance_to(
                   pg.Vector2(self.start_x, self.start_y)) > speed_factor):
                self.goal = pg.Vector2(self.start_x, self.start_y)
            gx, gy = tuple(self.goal)
            if ((abs(cur_x-gx) < speed_factor)
               and (abs(cur_y-gy) < speed_factor)):
                self.mode = GhostMode.CHASE
        elif self.mode == GhostMode.FRIGHTENED:

            l_ = self.game.map.get_direction_for_cell(cur_x, cur_y)

            if (len(l_) > 1
               and ((self.dx != 0) or (self.dy != 0))
               and ((-self.dx, -self.dy) in l_)):
                l_.remove((-self.dx, -self.dy))

            dx, dy = random.choice(l_)
            new_goal = self.adjust_vector(pg.Vector2(cur_x + dx, cur_y + dy))

            if (new_goal == self.get_player_pos()
               and ((self.dx != 0) or (self.dy != 0))):
                new_goal = self.adjust_vector(
                    pg.Vector2(cur_x - self.dx, cur_y - self.dy))

            self.goal = new_goal

        else:
            if not (self.goal is None):
                gx, gy = tuple(self.goal)
            else:
                gx, gy = (0, 0)
            if ((self.goal is None)
               or ((abs(cur_x-gx) < speed_factor)
                   and (abs(cur_y-gy) < speed_factor))):
                # We have reached the goal and we need a new one
                x_g = random.randrange(0, self.game.map.cols)
                y_g = random.randrange(0, self.game.map.rows)
                i = 20
                while (not self.game.map.has_cell_exit(x_g, y_g) and i > 0):
                    x_g = random.randrange(0, self.game.map.cols)
                    y_g = random.randrange(0, self.game.map.rows)
                    i -= 1
                if i > 0:
                    self.goal = pg.Vector2(x_g, y_g)

    def movement(self) -> None:
        """Update ghost movement vector and position for one frame."""

        keys = pg.key.get_pressed()

        if self.old_keys != keys:
            self.old_keys = keys
            if self.game.config.cheat:
                if keys[pg.K_f]:
                    self.mode = GhostMode.SCATTER
                if keys[pg.K_7]:
                    if self.mode == GhostMode.SCATTER:
                        self.mode = GhostMode.STROLL
                    elif self.mode == GhostMode.STROLL:
                        self.mode = GhostMode.CHASE
                    else:
                        self.mode = GhostMode.SCATTER
                    print(self.name, "x:", self.x, ", y:",
                          self.y, ", visible:", self.visible,
                          "goal:", self.goal)
                if keys[pg.K_3]:
                    self.freeze = not (self.freeze)

        x: float = float(self.x)
        y: float = float(self.y)

        speed_factor = self.get_speed_factor()

        if self.freeze:
            if self.mode == GhostMode.SPAWN:
                if ((not (self.goal is None))
                   and self.goal.distance_to(
                       pg.Vector2(x, y)) < speed_factor * 2):
                    self.reborn()
            return

        x_i = round(x)
        y_i = round(y)
        if (((abs(x_i - x) < speed_factor)
             and (abs(y_i - y) < speed_factor))):

            if self.mode == GhostMode.SPAWN and not (self.goal is None):
                gx, gy = tuple(self.goal)

                if ((abs(x_i-gx) < speed_factor)
                   and (abs(y_i-gy) < speed_factor)):
                    self.reborn()
                    return
            else:
                self.find_goal()

            # Check if player near and not ghosts etable now

            if self.goal is None:
                return

            P_ = self.game.map.find_path(
                (x_i, y_i), (int(self.goal.x), int(self.goal.y)))

            if len(P_) > 1:
                dx = P_[1][0] - x_i
                dx = int(dx > 0) - int(dx < 0)
                dy = P_[1][1] - y_i
                dy = int(dy > 0) - int(dy < 0)
                self.dx = dx
                self.dy = dy
            else:
                dx = 0
                dy = 0
        else:
            dx = self.dx
            dy = self.dy

        x = speed_factor * dx + self.x
        y = speed_factor * dy + self.y

        self.x = x
        self.y = y

    def update(self) -> None:
        """Advance timers, movement, animation, and collision handling."""

        if self.event_timer > 0:
            self.event_timer -= 1/FPS
            if self.event_timer <= 0:
                self.event_timer = 0
                self.event_end()
        self.movement()
        self.animation_timer += 0.1
        if self.animation_timer > 1:
            self.animation_timer = 0
            self.frame_index += 1
        if self.visible and self.collide_check(self.game.player):
            self.event()

    def event_end(self) -> None:
        """Resolve timed mode transitions when an event timer expires."""

        if self.mode == GhostMode.FRIGHTENED:
            self.mode = GhostMode.CHASE

    def event(self) -> None:
        """Handle collision outcome between ghost and player."""

        if not self.alive:
            return
        if self.game.config.cheat:
            print("Collide PacMan and", self.name, "!")
        if self.mode == GhostMode.FRIGHTENED:
            count_frightened = (
                1 +
                sum(
                 1 for n in self.game.npcs if n.mode != GhostMode.FRIGHTENED))
            self.game.score += self.points * count_frightened
            self.mode = GhostMode.DEAD
            self.alive = False
            self.dx = 0
            self.dy = 0
            sound = self.sounds.get(SoundType.EATEN, [])
            if len(sound) > 0:
                sound[0].play()

        else:
            if self.game.player.invincibil:
                return
            if self.game.player.alive:
                self.game.player.frame_index = 0
                sound = self.game.player.sounds.get(SoundType.EATEN, [])
                if len(sound) > 0:
                    sound[0].play()
            self.game.player.alive = False
            self.visible = False

    def after_death(self) -> None:
        """Drive dead ghost return-to-spawn behavior."""

        self.mode = GhostMode.SPAWN
        self.goal = pg.Vector2(self.start_x, self.start_y)
        speed_factor = self.get_speed_factor()

        if abs(round(self.x) - self.x) >= speed_factor:
            self.dx = 1 - 2 * ((round(self.x) - self.x) > 0)
        if abs(round(self.y) - self.y) >= speed_factor:
            self.dy = 1 - 2 * ((round(self.y) - self.y) > 0)

        # print(self.name, self.goal, (self.x, self.y), (self.dx, self.dy))

        if (abs(self.dx) > 0) and (abs(self.dy) > 0):
            if abs(self.dx) > abs(self.dy):
                self.dy = 0
            else:
                self.dx = 0

    def reborn(self) -> None:
        """Restore ghost to active chase state at spawn location."""

        self.mode = GhostMode.CHASE
        self.alive = True
        self.visible = True
        self.dx = 0
        self.dy = 0
        self.teleport()

    def get_player_pos(self) -> pg.Vector2:
        """Get player position snapped to map coordinates.

        Returns:
            pg.Vector2: Rounded player grid position.
        """
        return pg.Vector2(round(self.game.player.x), round(self.game.player.y))

    def get_player_direction(self) -> pg.Vector2:
        """Get normalized cardinal movement direction of the player.

        Returns:
            pg.Vector2: Direction vector on one axis, or zero vector.
        """

        if not self.game.player.dx and not self.game.player.dy:
            return pg.Vector2(0, 0)
        if abs(self.game.player.dx) > abs(self.game.player.dy):
            return pg.Vector2(1 if self.game.player.dx > 0 else -1, 0)
        return pg.Vector2(0, 1 if self.game.player.dy > 0 else -1)

    def adjust_vector(self, vector: pg.Vector2) -> pg.Vector2:
        """Clamp a vector to valid map bounds.

        Args:
            vector (pg.Vector2): Input map-space vector.

        Returns:
            pg.Vector2: Bounds-clamped vector.
        """

        max_x = self.game.map.cols - 1
        max_y = self.game.map.rows - 1
        x = min(max(vector.x, 0), max_x)
        y = min(max(vector.y, 0), max_y)
        return pg.Vector2(x, y)

    def sound_init(self) -> None:
        """Load or initialize ghost-specific sound effects."""

        self.sounds = Sound.read_sounds_from_files(
            "inc/sounds/ghosts/death/",
            SoundType.EATEN, self.sounds)

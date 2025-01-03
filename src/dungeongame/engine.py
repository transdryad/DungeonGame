from __future__ import annotations

from typing import TYPE_CHECKING
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from .input_handlers import Eventhandler

if TYPE_CHECKING:
    from entity import Actor, Entity
    from game_map import GameMap


class Engine:
    game_map: GameMap

    def __init__(self, player: Actor):
        self.event_handler: Eventhandler = Eventhandler(self)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(self.game_map.tiles["transparent"], (self.player.x, self.player.y), radius=8)
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context):
        self.game_map.render(console)
        context.present(console)
        console.clear()
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import tcod.event
from actions import Action, BumpAction, EscapeAction

if TYPE_CHECKING:
    from engine import Engine


class Eventhandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)
            if action is None:
                continue
            action.perform()
            self.engine.handle_enemy_turns()
            self.engine.update_fov()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym
        player = self.engine.player
        match key:
            case tcod.event.KeySym.UP | tcod.event.KeySym.w:
                action = BumpAction(player, dx=0, dy=-1)
            case tcod.event.KeySym.DOWN | tcod.event.KeySym.s:
                action = BumpAction(player, dx=0, dy=1)
            case tcod.event.KeySym.LEFT | tcod.event.KeySym.a:
                action = BumpAction(player, dx=-1, dy=0)
            case tcod.event.KeySym.RIGHT | tcod.event.KeySym.d:
                action = BumpAction(player, dx=1, dy=0)
            case tcod.event.KeySym.ESCAPE:
                action = EscapeAction(player)
        return action

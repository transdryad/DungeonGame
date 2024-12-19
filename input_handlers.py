from typing import Optional
import tcod.event
from actions import Action, EscapeAction, MovementAction


class Eventhandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym
        match key:
            case tcod.event.KeySym.UP | tcod.event.KeySym.w:
                action = MovementAction(dx=0, dy=-1)
            case tcod.event.KeySym.DOWN | tcod.event.KeySym.s:
                action = MovementAction(dx=0, dy=1)
            case tcod.event.KeySym.LEFT | tcod.event.KeySym.a:
                action = MovementAction(dx=-1, dy=0)
            case tcod.event.KeySym.RIGHT | tcod.event.KeySym.d:
                action = MovementAction(dx=1, dy=0)
            case tcod.event.KeySym.ESCAPE:
                action = EscapeAction()
        return action

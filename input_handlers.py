from typing import Optional
import tcod.event
from actions import Action, BumpAction, EscapeAction


class Eventhandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym
        match key:
            case tcod.event.KeySym.UP | tcod.event.KeySym.w:
                action = BumpAction(dx=0, dy=-1)
            case tcod.event.KeySym.DOWN | tcod.event.KeySym.s:
                action = BumpAction(dx=0, dy=1)
            case tcod.event.KeySym.LEFT | tcod.event.KeySym.a:
                action = BumpAction(dx=-1, dy=0)
            case tcod.event.KeySym.RIGHT | tcod.event.KeySym.d:
                action = BumpAction(dx=1, dy=0)
            case tcod.event.KeySym.ESCAPE:
                action = EscapeAction()
        return action

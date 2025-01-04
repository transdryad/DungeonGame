"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod
from tcod import libtcodpy

from .color import *
from .engine import Engine
from .entities import player as p, dagger as d, leather_armor as la
from .game_map import GameWorld
from .input_handlers import *

# Load the background image and remove the alpha channel.
BASE_DIR = os.path.dirname(__file__)
background_image = tcod.image.load(BASE_DIR + "/static/menu_background.png")[:, :, :3]


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(p)

    engine = Engine(player=player)

    engine.game_world = GameWorld(engine=engine, max_rooms=max_rooms, room_min_size=room_min_size,
                                  room_max_size=room_max_size,
                                  map_width=map_width, map_height=map_height)
    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message("Hello and welcome, adventurer, to yet another dungeon!", welcome_text)
    dagger = copy.deepcopy(d)
    leather_armor = copy.deepcopy(la)
    dagger.parent = player.inventory
    leather_armor.parent = player.inventory
    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)
    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)
    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)
        console.print(console.width // 2, console.height // 2 - 4, "DungeonGame", fg=menu_title,
                      alignment=libtcodpy.CENTER)
        console.print(console.width // 2, console.height - 2, "By Hazel Viswanath", fg=menu_title,
                      alignment=libtcodpy.CENTER)

        menu_width = 24
        for i, text in enumerate(["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]):
            console.print(console.width // 2, console.height // 2 - 2 + i, text.ljust(menu_width), fg=menu_text,
                          bg=black, alignment=libtcodpy.CENTER, bg_blend=libtcodpy.BKGND_ALPHA(64))

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.c:
            try:
                return MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.KeySym.n:
            return MainGameEventHandler(new_game())
        return None

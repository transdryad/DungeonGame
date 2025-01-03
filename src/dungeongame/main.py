#!/usr/bin/env/ python3
import copy

import tcod
import os

from .color import welcome_text
from .engine import Engine
from .entities import player as p
from .procgen import generate_dungeon


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    room_max_size = 16
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2
    BASE_DIR = os.path.dirname(__file__)
    tileset = tcod.tileset.load_tilesheet(BASE_DIR + "/static/sheet.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
    player = copy.deepcopy(p)
    engine = Engine(player=player)

    engine.game_map = generate_dungeon(max_rooms=max_rooms, room_min_size=room_min_size, room_max_size=room_max_size,
                                       map_width=map_width, map_height=map_height,
                                       max_monsters_per_room=max_monsters_per_room, engine=engine)
    engine.message_log.add_message("Hello and welcome, adventurer, to yet another dungeon!", welcome_text)
    engine.update_fov()

    with tcod.context.new_terminal(screen_width, screen_height, tileset=tileset, title="Dungeon Game",
                                   vsync=True) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)
            engine.event_handler.handle_events(context)

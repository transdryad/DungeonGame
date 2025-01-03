#!/usr/bin/env/ python3
import copy
import os

import tcod
import os

from .engine import Engine
from .entities import player as p
from .procgen import generate_dungeon


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = screen_width
    map_height = screen_height - 5

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
    engine.update_fov()

    with tcod.context.new_terminal(screen_width, screen_height, tileset=tileset, title="Dungeon Game",
                                   vsync=True) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)
            engine.event_handler.handle_events()

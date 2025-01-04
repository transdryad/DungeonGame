#!/usr/bin/env/ python3
import copy
import traceback

import tcod

from .color import welcome_text, error
from .exceptions import *
from .input_handlers import *
from .setup_game import *


def save_game(handler: BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")


def main() -> None:
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(BASE_DIR + "/static/sheet.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
    handler: BaseEventHandler = MainMenu()

    with tcod.context.new_terminal(screen_width, screen_height, tileset=tileset, title="Dungeon Game",
                                   vsync=True) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)
                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except (Exception,):  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, EventHandler):
                        handler.engine.message_log.add_message(traceback.format_exc(), error)
        except QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            save_game(handler, "savegame.sav")
            raise
        except BaseException:  # Save on any other unexpected exception.
            save_game(handler, "savegame.sav")
            raise

import tcod

from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

def main():
    screen_w = 80
    screen_h = 50

    map_w = 80
    map_h = 50

    tileset = tcod.tileset.load_tilesheet(
        'dejavu10x10_gs_tc.png', 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player = Entity(int(screen_w / 2), int(screen_h / 2), '@', (255, 255, 255))
    npc = Entity(int(screen_w / 2 - 5), int(screen_h / 2), '@', (255, 0, 255))
    entities = {player, npc}

    game_map = GameMap(map_w, map_h)

    engine = Engine(entities = entities, event_handler = event_handler, game_map = game_map, player = player)

    with tcod.context.new_terminal(
        screen_w,
        screen_h,
        tileset = tileset,
        title = 'Testing grounds for map generators',
        vsync = True,
    ) as context:
        root_console = tcod.Console(screen_w, screen_h, order = 'F')
        while True:
            engine.render(console = root_console, context = context)
            events = tcod.event.wait()
            engine.handle_events(events)

if __name__ == '__main__':
    main()
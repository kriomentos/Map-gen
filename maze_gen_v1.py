import random
from game_map import GameMap
import tile_types
import numpy as np

random.seed("UnkleDunkle")

def generate_maze_v1(map_w, map_h) -> GameMap:
    map_w = map_w // 2 * 2 + 1
    map_h = map_h // 2 * 2 + 1

    sx = random.choice(range(0, map_w -  1))
    sy = random.choice(range(0, map_h - 1))

    dungeon = GameMap(map_w, map_h)

    path = Maze(map_w, map_h)
    # path.tiles = np.pad(path.tiles, (1, 1), mode = 'constant', constant_values = tile_types.visited)
    path.create_maze(sx, sy)

    dungeon.tiles = path.tiles

    return dungeon

class Maze:
    def __init__(self, width, height):
        # ensures that sizing is odd | not required for algorithm to work
        self.width = width
        self.height = height
        # intialize map filled with walls that will be carved out
        self.tiles = np.full((self.width, self.height), fill_value = tile_types.wall, order = 'F')

    def set_path(self, x, y):
        # change the type of the tile at [x, y] to floor
        self.tiles[x, y] = tile_types.floor

    def set_wall(self, x, y):
        # change the type of the tile at [x, y] to wall
        self.tiles[x, y] = tile_types.wall

    def is_wall(self, x, y):
        # checks if tile at [x, y] is a wall and returns it if it is
        if 0 <= x < self.width and 0 <= y < self.height and self.tiles[x, y] == tile_types.wall:
            return self.tiles[x, y]
        else:
            return False

    def create_maze(self, x, y):
        self.set_path(x, y)
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        random.shuffle(directions)

        while len(directions) > 0:
            dir = directions.pop()
            node_x = x + (dir[0] * 2)
            node_y = y + (dir[1] * 2)

            if self.is_wall(node_x, node_y):
                mx = x + dir[0]
                my = y + dir[1]
                self.set_path(mx, my)
                self.create_maze(node_x, node_y)
        return
import random
import re
import traceback
from game_map import GameMap
import tile_types
import numpy as np
import sys

sys.setrecursionlimit(10000)

def generate_maze_v1(map_w, map_h) -> GameMap:
    # if map_w % 2 == 0:
    #     map_w -= 1
    # if map_h % 2 == 0:
    #     map_h -= 1
    dungeon = GameMap(map_w, map_h)

    # path = np.full((map_h - 1, map_w - 1), fill_value = tile_types.wall, order = 'F')

    # path[1::2, 1::2] = tile_types.floor
    # path[:,[0,-1]] = path[[0,-1]] = tile_types.visited

    # sx = random.choice(range(2, map_w - 2, 2))
    # sy = random.choice(range(2, map_h - 2, 2))

    # generate(path, sx, sy)

    # # path[path == tile_types.visited] = tile_types.floor
    # # maze.tiles[maze.tiles == tile_types.visited] = tile_types.floor

    # path = np.pad(path, (0, 1), mode = 'constant')
    path = Maze(map_w - 1, map_h - 1)
    path.tiles = np.pad(path.tiles, (0, 1), mode = 'constant')
    dungeon.tiles = path.tiles

    return dungeon

class Maze:
    def __init__(self, width, height):
        self.width = width // 2 * 2 + 1
        self.height = height // 2 * 2 + 1

        self.tiles = np.full((self.width, self.height), fill_value = tile_types.wall, order = 'F')

    def set_path(self, x, y):
        self.tiles[x, y] = tile_types.floor

    def set_wall(self, x, y):
        self.tiles[x, y] = tile_types.wall

    def is_wall(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
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
                print(f'node is a wall')
                mx = x + dir[0]
                my = y + dir[1]
                self.set_path(mx, my)

                self.create_maze(node_x, node_y)
        return

def generate(maze, cx, cy):
    maze[cx, cy] = tile_types.visited

    if(maze[cy - 2, cx] == tile_types.visited
    and maze[cy + 2, cx] == tile_types.visited
    and maze[cy, cx - 2] == tile_types.visited
    and maze[cy, cx + 2] == tile_types.visited):
        pass
    else:
        li = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        random.shuffle(li)
        while len(li) > 0:
            dir = li.pop()

            node_x = cx + (dir[0] * 2)
            node_y = cy + (dir[1] * 2)

            if is_wall(maze, node_x, node_y):
                print(f'node is a wall')
                mx = cx + dir
                my = cy + dir
                maze[mx, my] = tile_types.visited

                generate(maze, node_x, node_y)

        return

            # if dir == 1: # UP
            #     nx = cx
            #     mx = cx
            #     ny = cy - 2
            #     my = cy - 1
            # elif dir == 2: # DOWN
            #     nx = cx
            #     mx = cx
            #     ny = cy + 2
            #     my = cy + 1
            # elif dir == 3: # LEFT
            #     nx = cx - 2
            #     mx = cx - 1
            #     ny = cy
            #     my = cy
            # elif dir == 4: # RIGHT
            #     nx = cx + 2
            #     mx = cx + 1
            #     ny = cy
            #     my = cy

            # if self[ny, nx] != tile_types.visited:
            #     self[my, mx] = tile_types.visited
            #     generate(self, nx, ny)

def is_wall(self, x, y):
    if 0 <= x < self.shape[0] and 0 <= y < self.shape[1]:
        return self[x, y]
    else:
        return False
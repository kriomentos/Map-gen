from dataclasses import dataclass
from random import randint, getrandbits, choice, seed
from enum import Enum
import numpy as np

seed('UnkleDunkle')

UNUSED = -1
FLOOR = 1
CORRIDOR = 2
WALL = 3
CLOSEDDOOR = 4
OPENDOOR = 5
UPSTAIRS = 6
DOWNSTAIRS = 7

TILE_MAPPING = {
    UNUSED: ' ',
    FLOOR: '.',
    CORRIDOR: ',',
    WALL: '#',
    CLOSEDDOOR: '+',
    OPENDOOR: '-',
    UPSTAIRS: '<',
    DOWNSTAIRS: '>'
}

class Direction(Enum):
    North = 1,
    South = 2,
    West = 3,
    East = 4

class Rect:
    def __init__(self, x = None, y = None, width = None, height = None) -> None:
        self.x = x if x is not None else 1
        self.y = y if y is not None else 1
        self.width = width if width is not None else 1
        self.height = height if height is not None else 1

class Dungeon:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__tiles = [[UNUSED] * width for i in range(height)] # np.full((width, height), fill_value = UNUSED, order = 'F')
        self.__rooms = []
        self.__exits = [Rect]

    @property
    def __area(self):
        return self.__width * self.__height

    def getTile(self, x: int, y: int):
        if x < 0 or y < 0 or x >= self.__width or y >= self.__height:
            return UNUSED

        return self.__tiles[int(x)][int(y)]

    def setTile(self, x, y, tile):
        self.__tiles[int(x)][int(y)] = tile

    def selectFeature(self):
        for i in range(1000):
            if not self.__exits:
                break

            r = randint(0, len(self.__exits))
            x = randint(int(self.__exits[r].x), int(self.__exits[r].x + self.__exits[r].width - 1))
            y = randint(int(self.__exits[r].y), int(self.__exits[r].y + self.__exits[r].height - 1))

            for dir in Direction:
                if self.createFeature(x, y, dir):
                    self.__exits.pop(self.__exits[0] + r)
                    return True

            return False

    def createFeature(self, x, y, dir: Direction):
        roomChance = 0.5

        dx = 0
        dy = 0

        if dir == Direction.North:
            dy = 1
        elif dir == Direction.South:
            dy = -1
        elif dir == Direction.West:
            dx = 1
        elif dir == Direction.East:
            dx = -1

        if self.getTile(x + dx, y + dy) is not FLOOR and CORRIDOR:
            return False

        if randint(0, 1) < roomChance:
            if self.makeRoom(x, y, dir):
                self.setTile(x, y, CLOSEDDOOR)
                return True
        else:
            if self.makeCorridor(x, y, dir):
                if self.getTile(x + dx, y + dy) == FLOOR:
                    self.setTile(x, y, CLOSEDDOOR)
                else:
                    self.setTile(x, y, CORRIDOR)

                return True

        return False

    def makeRoom(self, x, y, dir: Direction, firstRoom: bool = False):
        minSize = 3
        maxSize = 6

        room = Rect()
        room.width = randint(minSize, maxSize)
        room.height = randint(minSize, maxSize)

        if dir == Direction.North:
            room.x = x - room.width / 2
            room.y = y - room.height
        elif dir == Direction.South:
            room.x = x - room.width / 2
            room.y = y + 1
        elif dir == Direction.West:
            room.x = x - room.width
            room.y = y - room.height / 2
        elif dir == Direction.East:
            room.x = x + 1
            room.y = y - room.height / 2

        if self.placeRect(room, FLOOR):
            self.__rooms.append(room)

            if dir is not Direction.South or firstRoom:
                self.__exits.append(Rect(room.x, room.y - 1, room.width, 1))
            if dir is not Direction.North or firstRoom:
                self.__exits.append(Rect(room.x, room.y + room.height, room.width, 1))
            if dir is not Direction.West or firstRoom:
                self.__exits.append(Rect(room.x - 1, room.y, 1, room.height))
            if dir is not Direction.East or firstRoom:
                self.__exits.append(Rect(room.x + room.width, room.y, 1, room.height))

            return True

        return False

    def makeCorridor(self, x, y, dir: Direction):
        minCorridorLen = 3
        maxCorridorLen = 6

        corridor = Rect()
        corridor.x = x
        corridor.y = y

        if getrandbits(1):
            corridor.width = randint(minCorridorLen, maxCorridorLen)
            corridor.height = 1

            if dir == Direction.North:
                corridor.y = y - 1
                if getrandbits(1):
                    corridor.x = x - corridor.width + 1
            elif dir == Direction.South:
                corridor.y = y + 1
                if getrandbits(1):
                    corridor.x = x - corridor.width + 1
            elif dir == Direction.West:
                corridor.x = x - corridor.width
            elif dir == Direction.East:
                corridor.x = x + 1
        else:
            corridor.width = 1
            corridor.height = randint(minCorridorLen, maxCorridorLen)

            if dir == Direction.North:
                corridor.y = y - corridor.height
            elif dir == Direction.South:
                corridor.y = y + 1
            elif dir == Direction.West:
                corridor.x = x - 1
                if getrandbits(1):
                    corridor.y = y - corridor.height + 1
            elif dir == Direction.East:
                corridor.x = x + 1
                if getrandbits(1):
                    corridor.y = y - corridor.height + 1

        if self.placeRect(corridor, CORRIDOR):
            if dir is not Direction.South and corridor.width != 1:
                self.__exits.append(Rect(corridor.x, corridor.y - 1, corridor.width, 1))
            if dir is not Direction.North and corridor.width != 1:
                self.__exits.append(Rect(corridor.x, corridor.y + corridor.height, corridor.width, 1))
            if dir is not Direction.East and corridor.height != 1:
                self.__exits.append(Rect(corridor.x - 1, corridor.y, 1, corridor.height))
            if dir is not Direction.West and corridor.height != 1:
                self.__exits.append(Rect(corridor.x + corridor.width, corridor.y, 1, corridor.height))

            return True

        return False

    def placeRect(self, rect: Rect, tile):
        if rect.x < 1 or rect.y < 1 or rect.x + rect.width > self.__width - 1 or rect.y + rect.height > self.__height - 1:
            return False

        y = rect.y
        x = rect.x
        print(f'x: {x}')
        while y < rect.y + rect.height:
            while x < rect.x + rect.width:
                if self.getTile(x, y) is not UNUSED:
                    return False
                x += 1
            y += 1


        while y - 1 < rect.y + rect.height + 1:
            while x - 1 < rect.x + rect.width + 1:
                if x == rect.x - 1 or y == rect.y - 1 or x == rect.x + rect.width or y == rect.y + rect.height:
                    self.setTile(x, y, WALL)
                else:
                    self.setTile(x, y, tile)
                x += 1
            y += 1

        return True

    def generate(self, maxFeatures):
        if not self.makeRoom(self.__width / 2, self.__height / 2, choice(list(Direction)), True):
            print(f'Can\'t place first room')

        for i in range(maxFeatures):
            if not self.selectFeature():
                print(f'Can\'t place more features (placed {i})\n')
                break

        for tile in self.__tiles:
            if tile == UNUSED:
                tile = ','
            elif tile == FLOOR or tile == CORRIDOR:
                tile = ' '

    def print(self):
        for i in range(self.__height):
            for j in range(self.__width):
                print(f'{self.getTile(i, j)}')
            print(f'\n')

    def print_grid(self):
        print("_ " * self.__width + '\n\n' + 'Grid map\n' + '_ ' * self.__width, end = '\n\n\n')

        # quite old way of printing out grids
        # for r in range(self.__rows):
        #   for c in range(self.__cols):
        #       print('{}'.format(self.tile_content(r, c)), end=' ')
        #   print('\n')

        # much better and 'new' approach thanks to Uncle
        print('\n'.join(
            (self.__get_row_as_string(row) for row in self.__tiles)
        ), end = '\n\n')

        f = open('grid_output.txt', 'w')
        f.write('\n\n')
        f.write('\n'.join(
            (self.__get_row_as_string(row) for row in self.__tiles)
        ))
        f.close()

    def __get_row_as_string(self, row):
        return ' '.join((TILE_MAPPING[cell] for cell in row))

if __name__ == '__main__':
    cave = Dungeon(30, 40)
    cave.generate(50)
    cave.print_grid()
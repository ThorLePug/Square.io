import pygame


class Block:
    type = ''
    width = 16
    height = 16
    colour = (0, 0, 0)
    collide = True

    def __init__(self, x: int, y: int) -> None:
        self.type = self.__class__.__name__
        self.colour = self.colour
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def __repr__(self):
        return f'{self.type}(pos : {self.rect.center})'

    def render(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)


class Wall(Block):
    colour = (150, 150, 150)


class Ground(Block):
    colour = (0, 0, 0)
    collide = False


BLOCK_TYPES = {
                1: Wall,
                0: Ground
              }


def load_map() -> list:
    f = open('maps/map.txt', 'r')
    data = f.read()
    f.close()
    game_data = []
    data = data.split("\n")
    for row in data:
        game_data.append(list(row))
    return game_data


def create_map(map_list: list):
    map_object = []
    x_offset = 0
    y_offset = 0
    for row in map_list:
        map_object.append([])
        for block in row:
            tile = BLOCK_TYPES[int(block)](x_offset*16, y_offset*16)
            map_object[y_offset].append(tile)
            x_offset += 1
        y_offset += 1
        x_offset = 0
    return map_object.copy()


class TPBlock(Block):
    colour = (255, 0, 255)

import pygame


def load_map() -> list:
    f = open('../maps/map.txt', 'r')
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
            tile = Block(x_offset*16, y_offset*16, int(block))
            map_object[y_offset].append(tile)
            x_offset += 1
        y_offset += 1
        x_offset = 0
    return map_object.copy()


class Block:
    def __init__(self, x, y, id_block: int) -> None:
        self.block_types = {
            0: 'air',
            1: 'wall'
        }
        self.x = x
        self.y = y

        self.width = 16
        self.height = 16
        self.id = id_block
        self.type = self.block_types[self.id]
        self.colour = pygame.Color((155, 155, 155))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.mask = pygame.mask.Mask(size=(self.width, self.height))

    def render(self, surface):
        if self.id != 0:
            pygame.draw.rect(surface, self.colour, self.rect)


class TPBlock(Block):
    def __init__(self, x, y, id_block: int):
        super().__init__(x, y, id_block)
        self.map_target = 1

# BEING BUILT --------------------------------------------- #


class Map:
    def __init__(self, path):
        self.walls = []





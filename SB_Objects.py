import os

image_path = os.getcwd() + '/game_objects/images/'
list_of_walls = []
list_of_walls_on_the_map = []


class Wall:
    def __init__(self, name, pattern, tiles, walkable, destructible, game_image, cordx, cordy):
        self.name = name
        self.pattern = pattern
        self.tiles = tiles
        self.type = 'Wall'
        self.walkable = walkable
        self.destructible = destructible
        self.game_image = image_path + game_image
        self.cordx = cordx
        self.cordy = cordy


stone_wall = Wall('Stone Wall', 0, 0, False, False, 'swall.png', 0, 0)

list_of_walls.append(stone_wall)


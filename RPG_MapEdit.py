# Simple map editor for this project

import os
game_map = []
list_of_furniture = []


class Furniture:
    def __init__(self, name, durability, map_repr):
        self.name = name
        self.durability = durability
        self.map_repr = map_repr
        self.x = 0
        self.y = 0

    def make_new(self, name, durability, map_repr):
        new_furniture = Furniture(name, durability, map_repr)
        list_of_furniture.append(new_furniture)

    def place_item(self):
        placed = False

        while not placed:
            key = input('Where do you want to place me ?')
            if key == 'W':
                game_map[self.x][self.y] = 0
                self.x -= 1
                game_map[self.x][self.y] = self.map_repr
            elif key == 'S':
                game_map[self.x][self.y] = 0
                self.x += 1
                game_map[self.x][self.y] = self.map_repr
            elif key == 'A':
                game_map[self.x][self.y] = 0
                self.y -= 1
                game_map[self.x][self.y] = self.map_repr
            elif key == 'D':
                game_map[self.x][self.y] = 0
                self.y += 1
                game_map[self.x][self.y] = self.map_repr
            elif key == '-DONE':
                placed = True
            map_render()


def load_map():
    map_name = input('Please type the name of the file: ')
    filepath = os.path.join('C:/Users/Andreas/Desktop/' + str(map_name))
    with open(filepath + '.txt', 'r') as file:
        data = file.readlines()
        height = data[0]
        width = data[1]
        global game_map
        game_map = [[0 for x in range(0, int(width[8:]))] for x in range(0, int(height[9:]))]


def save_map():
    map_name = input('Please name your map: ')
    filepath = os.path.join('C:/Users/Andreas/Desktop/' + str(map_name))
    with open(filepath + '.txt', 'w') as f:
        f.write('height = 10 \n')
        f.write('width = 10 \n')


def create_map():
    set_size = False
    while not set_size:
        set_height = input('Please enter the value(1 - 10) for the width of the map: ')
        set_width = input('Please enter the value(1 - 10) for the height of the map: ')
        if 0 < int(set_height) <= 10:
            if 0 < int(set_width) <= 10:
                global game_map;
                game_map = [[0 for x in range(0, int(set_width))] for x in range(0, int(set_height))]
                set_size = True


def map_render():
    rendered = ''
    counter = 0
    for x in game_map:
        for y in x:
            counter += 1
            if y == 0:
                rendered += '[ ]'
            else:
                rendered += '[' + str(y) + ']'
            if counter == len(game_map):
                rendered += '\n'
                counter = 0

    print(rendered)


def render_list_of():
    list_of_names = []
    for x in list_of_furniture:
        list_of_names.append(x.name)
    return list_of_names


def main():
    Exit = False
    while not Exit:
        select = input('Please choose what you want to do(For help type -H): ')
        if select == '-H':
            print('''If you want to build a new map, type "-CREATE"
        If you want to load in some map, type "-LOAD name_of_the_file"
        If you want to save your map, type "-SAVE name_of_the_file"''')
        elif select == '-CREATE':
            create_map()
        elif select == '-LOAD':
            load_map()
        elif select == '-SAVE':
            save_map()
        elif select == '-FURNITURE':
            options = input('Would you like to place or create new furniture ?')
            if options == '-PLACE':
                item = input('Which piece of furniture would you like to pick?')
                for obj in list_of_furniture:
                    if obj.name == item:
                        game_map[obj.x][obj.y] = obj.map_repr
                        map_render()
                        obj.place_item()
            elif options == '-CREATE':
                name = input('How would you like to name it ?')
                durability = input('How durable should it be ?')
                map_repr = input('How should it be visible as on the map ?')
                Furniture.make_new(name, durability, map_repr)

        elif select == '-EXIT':
            Exit = True

        map_render()
        print(render_list_of())



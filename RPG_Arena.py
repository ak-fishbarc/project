# This is the skeleton of the main project
# As it was a draft version, it might not be the cleanest

import random as rnd
import os
import csv
import RPG_Items_DB


class Player:
    def __init__(self, name, level, exp, clasT):
        self.name = name
        self.level = level
        self.exp = exp
        self.clasT = clasT
        self.dmg = 1
        self.armr = 1
        self.dodge = 1 + self.clasT.agi
        self.map_repr = 'P'
        self.x = 4
        self.y = 8
        self.hp = self.clasT.hp
        self.inv = []
        self.equipped = []

    def measure_power(self, other):
        deal_dmg = (self.dmg + self.clasT.strg) - (other.armr + other.dodge)
        return deal_dmg

    def move_around(self, key):
        game_map[self.x][self.y] = 0
        key = key
        if key == 'W':
           if game_map[self.x - 1][self.y] == 0:
              self.x -= 1
        elif key == 'S':
           if game_map[self.x + 1][self.y] == 0:
              self.x += 1
        elif key == 'A':
           if game_map[self.x][self.y - 1] == 0:
              self.y -= 1
        elif key == 'D':
           if game_map[self.x][self.y + 1] == 0:
              self.y += 1

        return map_render()

    def display_inventory(self):
        print('Inventory: ')
        Inventory = ' '
        for item in self.inv:
            Inventory += '[' + str(item.name) + ']'
        print(Inventory)

    def equip_item(self, name):
        for item in self.inv:
            if item.name == name:
                print(f'{item.name} equipped!')
                self.inv.remove(item)
                self.equipped.append(item)
                if item.obj_type == 'Weapon':
                   if item in self.equipped:
                       print(self.dmg)
                       self.dmg += item.power
                       print(self.dmg)

    def unequip_item(self, name):
        for item in self.equipped:
            if item.name == name:
                print(f'{item.name} unequipped!')
                self.equipped.remove(item)
                self.inv.append(item)
                if item.obj_type == 'Weapon':
                    print(self.dmg)
                    self.dmg -= item.power
                    print(self.dmg)

    def pick_up_loot(self):
        for loot in list_of_loot:
            if game_map[self.x-1][self.y] or game_map[self.x+1][self.y] \
               or game_map[self.x][self.y-1] or game_map[self.y+1]      \
               == game_map[loot.x][loot.y]:
               game_map[loot.x][loot.y] = 0
               self.inv.append(loot.contains[0])
               list_of_loot.remove(loot)
               loot.x = 0
               loot.y = 0

        return map_render()


class ClassTemplate:
    def __init__(self, name, strg, agi, intel, hp):
        self.name = name
        self.strg = strg
        self.agi = agi
        self.intel = intel
        self.hp = hp


class MonsterTemplate:
    def __init__(self, name, strg, agi, intel, hp, dmg, armr):
        self.name = name
        self.strg = strg
        self.agi = agi
        self.intel = intel
        self.hp = hp
        self.dmg = 1 + dmg
        self.armr = armr
        self.dodge = 1 + agi
        self.map_repr = 'O'
        self.x = 1
        self.y = 5
        self.dead = False

    def measure_dmg(self, other):
        deal_dmg = (self.strg + self.dmg) - (other.armr + other.dodge)
        return deal_dmg

    def move_around(self, other):
        if self.hp <= 0:
           list_of_objects.remove(self)
           self.dead = True
           game_map[self.x][self.y] = 0

        if self.dead == False:
           if game_map[self.x - 1][self.y] == game_map[other.x][other.y] or \
           game_map[self.x + 1][self.y] == game_map[other.x][other.y] or \
           game_map[self.x][self.y - 1] == game_map[other.x][other.y] or \
           game_map[self.x][self.y + 1] == game_map[other.x][other.y]:
             fight(self, other)
           else:
              game_map[self.x][self.y] = 0
           if other.x != self.x:
              if other.x < self.x:
                  if game_map[self.x - 1][self.y] == 0:
                     self.x -= 1
              elif game_map[self.x + 1][self.y] == 0:
                     self.x += 1
           if other.y != self.y:
              if other.y < self.y:
                  if game_map[self.x][self.y - 1] == 0:
                     self.y -= 1
              elif game_map[self.x][self.y + 1] == 0:
                     self.y += 1
           game_map[self.x][self.y] = self.map_repr
        else:
           self.drop_loot()

    def drop_loot(self):
        create_loot = Loot_Drop(1, self.x, self.y)
        create_loot.define_loot()
        game_map[self.x][self.y] = create_loot.map_repr
        list_of_loot.append(create_loot)


class Loot_Drop:
    def __init__(self, size, x, y):
       self.size = size
       self.map_repr = 'b'
       self.x = x
       self.y = y
       self.contains = []
       self.loot = True

    def define_loot(self):
        if self.size == 1:
           self.contains.append(RPG_Items_DB.Broad_Sword)


barbarian = ClassTemplate('barbarian', 10, 5, 2, 100)
player1 = Player('Rookie', 1, 0, barbarian)
orc = MonsterTemplate('Orc', 16, 2, 1, 12, 6, 3)

list_of_loot = []

list_of_objects = []
list_of_objects.append(player1)
list_of_objects.append(orc)

game_map = [[0 for x in range(0, 10)] for x in range(0, 10)]


def fight(obj1, obj2):
    dmg1 = obj1.measure_dmg(obj2)
    dmg2 = obj2.measure_power(obj1)
    obj1.hp -= dmg2
    obj2.hp -= dmg1


def map_render():
    rendered = ''
    counter = 0
    for object in list_of_objects:
        if object.x and object.y:
            game_map[object.x][object.y] = object.map_repr
    for x in game_map:
        for y in x:
             counter += 1
             if y == 0:
                 rendered += '[ ]'
             else:
                 rendered += '[' + str(y) + ']'
             if counter == 10:
                rendered += '\n'
                counter = 0

    print(rendered)


def save_game(save_name):
    filepath = os.path.join('C:/Users/Andreas/Desktop/' + str(save_name))
    with open(filepath + '.csv', 'w') as f:
        save_data = csv.writer(f, delimiter=',', quotechar='|')
        for object in list_of_objects:
            save_data.writerow(['Player1', [object.x], [object.y]])


def load_game(load_name):
    filepath = os.path.join('C:/Users/Andreas/Desktop/' + str(load_name))
    with open(filepath + '.csv', 'r') as f:
         read_data = csv.reader(f, delimiter=',', quotechar='|')
         for row in read_data:
             for x in row:
                 if x == 'Player1':
                     load_x = str(row[1:2]).strip("[]'")
                     load_y = str(row[2:3]).strip("[]'")
                     game_map[player1.x][player1.y] = 0
                     player1.x = int(load_x)
                     player1.y = int(load_y)
                     map_render()


def main():
    Exit = False
    map_render()

    while not Exit:
        map_render()
        player1.display_inventory()
        key = input('Move: ')
        player1.move_around(key)
        for object in list_of_objects:
            object.move_around(player1)
        if key == '-PICK':
            player1.pick_up_loot()
        elif key == '-EQUIP':
            item_name = input('Which item ?')
            player1.equip_item(item_name)
        elif key == '-UNEQUIP':
            item_name = input('Which item?')
            player1.unequip_item(item_name)
        elif key == '-SAVE':
            name = input('Name: ')
            save_game(name)
        elif key == '-LOAD':
            name = input('Name: ')
            load_game(name)
        elif key == '-EXIT':
            Exit = True
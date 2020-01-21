import os

import SB_Professions as SBP
import SB_Equipment as SBE

image_path = os.getcwd() + "/creatures/images/"
list_of_players = []
list_of_monsters = []
list_of_monster_on_the_map = []
list_of_players_on_the_map = []


class Player:

    def __init__(self, name, level, profession, game_image, id_tag, cordx, cordy):
        self.name = name
        self.level = level
        self.type = "Creature"
        self.profession = profession
        self.game_image = image_path + game_image
        self.id_tag = id_tag
        self.is_dead = False

        self.strength = 0
        self.dexterity = 0
        self.endurance = 0
        self.intelligence = 0
        self.wisdom = 0
        self.health = 0
        self.armor = 0

        self.cordx = cordx
        self.cordy = cordy
        self.pathfinding = []
        self.inventory = []
        # Inventory window object
        self.show_inventory_win = None
        self.loot = None
        self.set_stats()

    def set_stats(self):
        self.strength = 0 + self.profession.strength
        self.dexterity = 0 + self.profession.dexterity
        self.endurance = 0 + self.profession.endurance
        self.intelligence = 0 + self.profession.intelligence
        self.wisdom = 0 + self.profession.wisdom
        self.health = 0 + self.profession.health
        self.armor = 0 + self.profession.armor


New_Player = Player("", 1, SBP.Barbarian, 'robe.png', 1, 0, 0)

list_of_players.append(New_Player)


class Monster(Player):

    def drop_loot(self):
        pass


Goblin = Monster("Goblin", 1, SBP.Barbarian, 'goblin.png', 0, 0, 0)

list_of_monsters.append(Goblin)

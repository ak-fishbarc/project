import random as rnd
import os

''' list_of_items, later on to be replaced by separate list of items for each item type.'''
list_of_items = []
item_image_path = os.getcwd() + "\item_images"

class LootContainer:

    def __init__(self, name, rarity, ingame_image):
        self.name = name
        # Object type for in-game checks. #
        self.object_type = "Container"
        # Type of item #
        self.item_type = "Loot"
        self.rarity = rarity
        self.loot_list = []
        self.ingame_image = item_image_path + ingame_image

    def create_loot(self):
        how_many_items = rnd.randint(0, 100)
        if how_many_items <= 2:
            number_of_items = 5
        elif how_many_items <= 5:
            number_of_items = 4
        elif how_many_items <= 15:
            number_of_items = 3
        elif how_many_items <= 30:
            number_of_items = 2
        elif how_many_items <= 75:
            number_of_items = 1
        else:
            number_of_items = 0

        while len(self.loot_list) < number_of_items:
            item_index = rnd.randint(0, len(list_of_items) - 1)
            # Pick random item from item list, by list index #
            if list_of_items[item_index].name == 'Gold Coins':
                # Roll for amount of gold #
                luck = rnd.randint(0, 100)
                if luck <= 33:
                    number_of_coins = rnd.randint(1, 5)
                elif luck <= 66:
                    number_of_coins = rnd.randint(6, 10)
                elif luck <= 89:
                    number_of_coins = rnd.randint(11, 15)
                elif luck <= 99:
                    number_of_coins = rnd.randint(16, 20)
                elif luck <= 100:
                    number_of_coins = rnd.randint(21, 25)
                ''' If one of the items in the container is already a gold coin, stack
                    them together. Another option:
                    If there is some gold in the container already, re-roll the item.
                    if list_of_items[item_index] not in self.loot_list:
                        list_of_items[item_index].item_stack += number_of_coins
                        self.loot_list.append(list_of_items[item_index])'''
                if len(self.loot_list) != 0:
                    if list_of_items[item_index] in self.loot_list:
                        list_of_items[item_index].item_stack += number_of_coins
                        number_of_items -= 1
                    else:
                        list_of_items[item_index].item_stack = number_of_coins
                        self.loot_list.append(list_of_items[item_index])
                else:
                    list_of_items[item_index].item_stack = number_of_coins
                    self.loot_list.append(list_of_items[item_index])
            else:
                self.loot_list.append(list_of_items[item_index])


class Item:

    def __init__(self, name, item_type, inventory_image, description):
        self.name = name
        # Object type for in-game checks, like collision checks etc. #
        self.object_type = "Item"
        # Type of item sword, mace, dagger etc #
        self.item_type = item_type
        self.inventory_image = item_image_path + inventory_image
        self.description = description
        self.item_stack = 0

    def dmg_1d4(self):
        damage = rnd.randint(1, 4)
        return damage

    def dmg_1d6(self):
        damage = rnd.randint(1, 6)
        return damage

    def dmg_1d8(self):
        damage = rnd.randint(1, 8)
        return damage


#  Items  #
dagger = Item("Dagger", "Daggers", "/dagger.png", "This dagger can deal 1k4 damage.")
short_sword = Item("Shortsword", "Swords", "/shortsword.png", "This sword deals 1k6 damage.")
long_sword = Item("Longsword", "Swords", "/longsword.png", "This sword deals 1k8 damage.")
mace = Item("Mace", "Mace", "/mace.png", "This mace deals 1k6 damage.")
pike = Item("Pike", "Spear", "/pike.png", "This pike deals 1k6 damage.")
gold_coin = Item("Gold Coins", "Coins", "", "")

list_of_items.append(dagger)
list_of_items.append(short_sword)
list_of_items.append(long_sword)
list_of_items.append(mace)
list_of_items.append(pike)
list_of_items.append(gold_coin)

# Loot  Containers  #
small_bag = LootContainer("Small Bag", "Common", "smallbag.png")
small_bag.create_loot()




class Item:
    def __init__(self, name, obj_type, power, lvl):
        self.name = name
        self.power = power
        self.obj_type = obj_type
        self.level = lvl

        if self.level == 1:
            self.bonus = 3


Broad_Sword = Item('Broad Sword', 'Weapon', 1, 1)
list_of_items = []
list_of_items.append(Broad_Sword)
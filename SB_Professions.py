list_of_professions = []


class Profession:

    def __init__(self, name, strength, dexterity, endurance, intelligence,
                 wisdom, charisma, health, armor):
        self.name = name
        self.strength = strength
        self.dexterity = dexterity
        self.endurance = endurance
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.health = health
        self.armor = armor


Barbarian = Profession("Barbarian", 10, 8, 10, 5, 5, 5, 100, 4)
Wizard = Profession("Wizard", 5, 5, 5, 10, 8, 6, 60, 0)

list_of_professions.append(Barbarian)
list_of_professions.append(Wizard)

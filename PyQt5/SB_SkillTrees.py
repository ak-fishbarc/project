import random as rnd
import os

skill_image_path = os.getcwd() + "/skill_icons"
list_of_trees = []


class Skill:

    def __init__(self, name, type, tier, shape, spell_range, skill_icon):
        self.name = name
        self.type = type
        self.tier = tier
        self.shape = shape
        self.spell_range = spell_range
        # Use list for next/prev skill, as there might be one to many connection
        # between skills
        self.next_skill = []
        self.previous_skill = []
        self.skill_icon = skill_icon

    def link_skills(self, skill):
        skill.previous_skill.append(self)
        self.next_skill.append(skill)

    def dmg_1d6(self):
        damage = rnd.randint(1, 6)
        return damage


class SkillTree:

    def __init__(self, name):
        self.name = name
        self.tier1 = []
        self.tier2 = []
        self.tier3 = []
        self.tier4 = []
        self.tier5 = []

    def add_skill(self, skill):
        if skill.tier == 1:
            self.tier1.append(skill)
        elif skill.tier == 2:
            self.tier2.append(skill)
        elif skill.tier == 3:
            self.tier3.append(skill)
        elif skill.tier == 4:
            self.tier4.append(skill)
        elif skill.tier == 5:
            self.tier5.append(skill)

fire_ray = Skill('Fire Ray', 'Fire', 1, 'Line', 6, skill_image_path + '/fireray.png')
fireball = Skill('Fireball', 'Fire', 2, 'Line', 6, skill_image_path + '/fireball.png')

fire_ray.link_skills(fireball)

wizard_tree = SkillTree('Wizard')
wizard_tree.add_skill(fire_ray)
wizard_tree.add_skill(fireball)

throw_weapon = Skill('Throw Weapon', 'Physical', 1, 'Line', 3, skill_image_path + '/throwep.png')
heavy_swing = Skill('Heavy Swing', 'Physical', 2, 'Front', 3, skill_image_path + '/heavyswing.png')

throw_weapon.link_skills(heavy_swing)

barbarian_tree = SkillTree('Barbarian')
barbarian_tree.add_skill(throw_weapon)
barbarian_tree.add_skill(heavy_swing)

list_of_trees.append(wizard_tree)
list_of_trees.append(barbarian_tree)


import SB_WidgetsClass as SBWC
import SB_Characters as SBC
import SB_SpellList as SBSL
import SB_Objects as SBOB

class GameMap:
    def __init__(self):
        self.board = [[0 for x in range(0, 10)] for x in range(0, 10)]
        self.list_of_objects = []
        self.removed_list = []
        self.player_casting_spell = False

    def create_map(self, window_name):
        num_of_x = 0
        num_of_y = 0
        xpos = 175
        ypos = 50
        for x in self.board:
            for y in x:
                floor = SBWC.Label('floortile.png', window_name, xpos, ypos, '')
                floor.hide_tile()
                if y != 0:
                    
                    # Use removed list for labels of objects that are no longer active.
                    # Otherwise some objects will die / get destroyed and their labels
                    # will drain memory unused.
                    # Each time a new map is created, first use labels from the removed
                    # list. It would be different in case where the program would use
                    # respawning option as then labels would stick to objects.

                    if len(self.removed_list) == 0:

                        if self.board[num_of_x][num_of_y].type == 'Creature':
                            object_on_map = SBWC.Label(self.board[num_of_x][num_of_y].prof.game_image, window_name, xpos, ypos, self.board[num_of_x][num_of_y].name)
                            object_on_map.add_object(self.board[num_of_x][num_of_y])
                            self.list_of_objects.append(object_on_map)
                        elif self.board[num_of_x][num_of_y].type == 'Wall':
                            object_on_map = SBWC.Label(self.board[num_of_x][num_of_y].game_image, window_name, xpos, ypos, self.board[num_of_x][num_of_y].name)
                            object_on_map.add_object(self.board[num_of_x][num_of_y])
                            self.list_of_objects.append(object_on_map)
                    else:

                        if self.board[num_of_x][num_of_y].type == 'Creature':
                            self.removed_list[0].add_object(self.board[num_of_x][num_of_y])
                            self.removed_list[0].change_image(self.board[num_of_x][num_of_y].prof.game_image)
                            self.removed_list[0].change_id(self.board[num_of_x][num_of_y].name)
                            self.removed_list[0].move_self(xpos, ypos)
                            self.list_of_objects.append(self.removed_list[0])
                            self.removed_list.remove(self.removed_list[0])
                        else:
                            print('prryt')
                xpos += 50
                num_of_y += 1
            num_of_x += 1
            num_of_y = 0
            ypos += 50
            xpos = 175
        print(self.board)

    def move_player(self, direction):
        if direction == 'Up' and not self.player_casting_spell:
            if SBC.Player1.posx - 1 < 0:
                print('Oink')
            elif self.board[SBC.Player1.posx - 1][SBC.Player1.posy] == 0:
                self.board[SBC.Player1.posx][SBC.Player1.posy] = 0
                SBC.Player1.posx -= 1
                self.board[SBC.Player1.posx][SBC.Player1.posy] = SBC.Player1
                for item in self.list_of_objects:
                    if item.id == SBC.Player1.name:
                        item.y -= 50
                        item.move_self(item.x, item.y)
            elif self.board[SBC.Player1.posx - 1][SBC.Player1.posy] != 0:
                for item in self.list_of_objects:
                    if item.object.type == 'Container':
                        self.board[SBC.Player1.posx][SBC.Player1.posy] = 0
                        SBC.Player1.posx -= 1
                        SBC.Player1.pick_up_loot(item.object.loot_list)
                        self.board[SBC.Player1.posx][SBC.Player1.posy] = SBC.Player1
                        item.change_image('')
                        item.add_object('')
                        self.list_of_objects.remove(item)
                        self.removed_list.append(item)
                        for player in self.list_of_objects:
                            if player.id == SBC.Player1.name:
                                player.y -= 50
                                player.move_self(item.x, item.y)
                    else:
                        print('Oink')
            else:
                print('Oink')
        if direction == 'Down' and not self.player_casting_spell:
            if SBC.Player1.posx + 1 > 9:
                print('Oink')
            elif self.board[SBC.Player1.posx + 1][SBC.Player1.posy] == 0:
                self.board[SBC.Player1.posx][SBC.Player1.posy] = 0
                SBC.Player1.posx += 1
                self.board[SBC.Player1.posx][SBC.Player1.posy] = SBC.Player1
                for item in self.list_of_objects:
                    if item.id == SBC.Player1.name:
                        item.y += 50
                        item.move_self(item.x, item.y)
            elif self.board[SBC.Player1.posx + 1][SBC.Player1.posy] != 0:
                for item in self.list_of_objects:
                    if item.object.type == 'Container':
                        self.board[SBC.Player1.posx][SBC.Player1.posy] = 0
                        SBC.Player1.posx += 1
                        SBC.Player1.pick_up_loot(item.object.loot_list)
                        self.board[SBC.Player1.posx][SBC.Player1.posy] = SBC.Player1
                        item.change_image('')
                        item.add_object('')
                        self.list_of_objects.remove(item)
                        self.removed_list.append(item)
                        for player in self.list_of_objects:
                            if player.id == SBC.Player1.name:
                                player.y -= 50
                                player.move_self(item.x, item.y)
            else:
                print('Oink')
        if direction == 'Left' and not self.player_casting_spell:
            if SBC.Player1.posy - 1 < 0:
                print('Oink')
            elif self.board[SBC.Player1.posx][SBC.Player1.posy - 1] == 0:
                self.board[SBC.Player1.posx][SBC.Player1.posy] = 0
                SBC.Player1.posy -= 1
                self.board[SBC.Player1.posx][SBC.Player1.posy] = SBC.Player1
                for item in self.list_of_objects:
                    if item.id == SBC.Player1.name:
                        item.x -= 50
                        item.move_self(item.x, item.y)
            elif self.board[SBC.Player1.posx][SBC.Player1.posy - 1] != 0:
                for item in self.list_of_objects:
                    if item.object.type == 'Container':
                        self.board[SBC.Player1.posx][SBC.Player1.posy] = 0
                        SBC.Player1.posy -= 1
                        SBC.Player1.pick_up_loot(item.object.loot_list)
                        self.board[SBC.Player1.posx][SBC.Player1.posy] = SBC.Player1
                        item.change_image('')
                        item.add_object('')
                        self.list_of_objects.remove(item)
                        self.removed_list.append(item)
                        for player in self.list_of_objects:
                            if player.id == SBC.Player1.name:
                                player.y -= 50
                                player.move_self(item.x, item.y)
            else:
                print('Oink')
        if direction == 'Right' and not self.player_casting_spell:
            if SBC.Player1.posy + 1 > 9:
                print('Oink')
            elif self.board[SBC.Player1.posx][SBC.Player1.posy + 1] == 0:
                self.board[SBC.Player1.posx][SBC.Player1.posy] = 0
                SBC.Player1.posy += 1
                self.board[SBC.Player1.posx][SBC.Player1.posy] = SBC.Player1
                for item in self.list_of_objects:
                    if item.id == SBC.Player1.name:
                        item.x += 50
                        item.move_self(item.x, item.y)
            elif self.board[SBC.Player1.posx][SBC.Player1.posy + 1] != 0:
                for item in self.list_of_objects:
                    if item.object.type == 'Container':
                        self.board[SBC.Player1.posx][SBC.Player1.posy] = 0
                        SBC.Player1.posy += 1
                        SBC.Player1.pick_up_loot(item.object.loot_list)
                        self.board[SBC.Player1.posx][SBC.Player1.posy] = SBC.Player1
                        item.change_image('')
                        item.add_object('')
                        self.list_of_objects.remove(item)
                        self.removed_list.append(item)
                        for player in self.list_of_objects:
                            if player.id == SBC.Player1.name:
                                player.x += 50
                                player.move_self(item.x, item.y)
            else:
                print('Oink')
        if direction == 'CastSpell':
            self.player_casting_spell = True
        if self.player_casting_spell:
            if direction == 'Up':
                spell_to_cast = SBSL.fire_ray
                how_far = [x for x in range(1, spell_to_cast.spell_range)]
                for num in how_far:
                    index_x = SBC.Player1.posx - num
                    if index_x <= len(self.board) - 1:
                        affected_area = self.board[index_x][SBC.Player1.posy]
                        if affected_area != 0:
                            for item in self.list_of_objects:
                                if item.object.type == 'Creature':
                                    if item.object.name != SBC.Player1.name:
                                        item.object.hp -= spell_to_cast.k6()
                                        print(item.object.name)
                                        print(item.object.hp)
                                        if item.object.hp <= 0:
                                            item.object.is_dead = True
                                            item.object.drop_loot()
                                            self.board[item.object.posx][item.object.posy] = item.object.loot
                                            item.add_object(item.object.loot)
                                            print(item.object)
                                            item.change_image('smallbag.png')
                self.player_casting_spell = False
            if direction == 'Down':
                spell_to_cast = SBSL.fire_ray
                how_far = [x for x in range(1, spell_to_cast.spell_range)]
                for num in how_far:
                    index_x = SBC.Player1.posx - num
                    if index_x <= len(self.board) + 1:
                        affected_area = self.board[index_x][SBC.Player1.posy]
                        if affected_area != 0:
                            for item in self.list_of_objects:
                                if item.object.type == 'Creature':
                                    if item.object.name != SBC.Player1.name:
                                        item.object.hp -= spell_to_cast.k6()
                                        print(item.object.name)
                                        print(item.object.hp)
                                        if item.object.hp <= 0:
                                            item.object.is_dead = True
                                            item.object.drop_loot()
                                            self.board[item.object.posx][item.object.posy] = item.object.loot
                                            item.add_object(item.object.loot)
                                            print(item.object)
                                            item.change_image('smallbag.png')
                self.player_casting_spell = False
            if direction == 'Left':
                spell_to_cast = SBSL.fire_ray
                how_far = [x for x in range(1, spell_to_cast.spell_range)]
                for num in how_far:
                    index_y = SBC.Player1.posy - num
                    if index_y <= len(self.board) - 1:
                        affected_area = self.board[SBC.Player1.posx][index_y]
                        if affected_area != 0:
                            for item in self.list_of_objects:
                                if item.object.type == 'Creature':
                                    if item.object.name != SBC.Player1.name:
                                        item.object.hp -= spell_to_cast.k6()
                                        print(item.object.name)
                                        print(item.object.hp)
                                        if item.object.hp <= 0:
                                            item.object.is_dead = True
                                            item.object.drop_loot()
                                            self.board[item.object.posx][item.object.posy] = item.object.loot
                                            item.add_object(item.object.loot)
                                            print(item.object)
                                            item.change_image('smallbag.png')
                self.player_casting_spell = False
            if direction == 'Right':
                spell_to_cast = SBSL.fire_ray
                how_far = [x for x in range(1, spell_to_cast.spell_range)]
                for num in how_far:
                    index_y = SBC.Player1.posy + num
                    if index_y <= len(self.board) + 1:
                        affected_area = self.board[SBC.Player1.posx][index_y]
                        if affected_area != 0:
                            for item in self.list_of_objects:
                                if item.object.type == 'Creature':
                                    if item.object.name != SBC.Player1.name:
                                        item.object.hp -= spell_to_cast.k6()
                                        print(item.object.name)
                                        print(item.object.hp)
                                        if item.object.hp <= 0:
                                            item.object.is_dead = True
                                            item.object.drop_loot()
                                            self.board[item.object.posx][item.object.posy] = item.object.loot
                                            item.add_object(item.object.loot)
                                            print(item.object)
                                            item.change_image('smallbag.png')
                self.player_casting_spell = False

    def move_monster(self):
        if not self.player_casting_spell:
            for item in self.list_of_objects:
                if item.object.type == 'Creature' and isinstance(item.object, SBC.Monster):
                    vessel = item.object
                    if vessel.name != SBC.Player1.name and vessel.type == 'Creature' and vessel.hp > 0:
                        if vessel.posx + 1 == SBC.Player1.posx and vessel.posy == SBC.Player1.posy:
                            self.fight(vessel, SBC.Player1)
                        elif vessel.posx - 1 == SBC.Player1.posx and vessel.posy == SBC.Player1.posy:
                            self.fight(vessel, SBC.Player1)
                        elif vessel.posx < SBC.Player1.posx:
                            if vessel.posx + 1 <= 9:
                                if self.board[vessel.posx + 1][vessel.posy] == 0:
                                    self.board[vessel.posx][vessel.posy] = 0
                                    vessel.posx += 1
                                    self.board[vessel.posx][vessel.posy] = vessel
                                    item.y += 50
                                    item.move_self(item.x, item.y)
                                elif self.board[vessel.posx + 1][vessel.posy].type == 'Wall':
                                    if vessel.posy < SBC.Player1.posy and self.board[vessel.posx][vessel.posy + 1] == 0:
                                        self.board[vessel.posx][vessel.posy] = 0
                                        vessel.posy += 1
                                        self.board[vessel.posx][vessel.posy] = vessel
                                        item.x += 50
                                        item.move_self(item.x, item.y)
                                    elif vessel.posy > SBC.Player1.posy and self.board[vessel.posx][vessel.posy - 1] == 0:
                                        self.board[vessel.posx][vessel.posy] = 0
                                        vessel.posy -= 1
                                        self.board[vessel.posx][vessel.posy] = vessel
                                        item.x -= 50
                                        item.move_self(item.x, item.y)

                            else:
                                print('Waka waka')
                        elif vessel.posx > SBC.Player1.posx:
                            if vessel.posx - 1 >= 0:
                                if self.board[vessel.posx - 1][vessel.posy] == 0:
                                    self.board[vessel.posx][vessel.posy] = 0
                                    vessel.posx -= 1
                                    self.board[vessel.posx][vessel.posy] = vessel
                                    item.y -= 50
                                    item.move_self(item.x, item.y)
                                elif self.board[vessel.posx - 1][vessel.posy].type == 'Wall':
                                    if vessel.posy < SBC.Player1.posy and self.board[vessel.posx][vessel.posy + 1] == 0:
                                        self.board[vessel.posx][vessel.posy] = 0
                                        vessel.posy += 1
                                        self.board[vessel.posx][vessel.posy] = vessel
                                        item.x += 50
                                        item.move_self(item.x, item.y)
                                    elif vessel.posy > SBC.Player1.posy and self.board[vessel.posx][vessel.posy - 1] == 0:
                                        self.board[vessel.posx][vessel.posy] = 0
                                        vessel.posy -= 1
                                        self.board[vessel.posx][vessel.posy] = vessel
                                        item.x -= 50
                                        item.move_self(item.x, item.y)
                            else:
                                print('Waka waka')
                        elif vessel.posx == SBC.Player1.posx and vessel.posy != SBC.Player1.posy:
                            if vessel.posy + 1 == SBC.Player1.posy:
                                self.fight(vessel, SBC.Player1)
                            elif vessel.posy - 1 == SBC.Player1.posy:
                                self.fight(vessel, SBC.Player1)
                            elif vessel.posy < SBC.Player1.posy:
                                if vessel.posy + 1 <= 9:
                                    if self.board[vessel.posx][vessel.posy + 1] == 0:
                                        self.board[vessel.posx][vessel.posy] = 0
                                        vessel.posy += 1
                                        self.board[vessel.posx][vessel.posy] = vessel
                                        item.x += 50
                                        item.move_self(item.x, item.y)
                                    elif self.board[vessel.posx][vessel.posy + 1].type == 'Wall':
                                        if vessel.posx < SBC.Player1.posx and self.board[vessel.posx + 1][vessel.posy] == 0:
                                            self.board[vessel.posx][vessel.posy] = 0
                                            vessel.posx += 1
                                            self.board[vessel.posx][vessel.posy] = vessel
                                            item.y += 50
                                            item.move_self(item.x, item.y)
                                        elif vessel.posy > SBC.Player1.posy and self.board[vessel.posx - 1][vessel.posy] == 0:
                                            self.board[vessel.posx][vessel.posy] = 0
                                            vessel.posx -= 1
                                            self.board[vessel.posx][vessel.posy] = vessel
                                            item.y -= 50
                                            item.move_self(item.x, item.y)
                                else:
                                    print('Waka waka')
                            elif vessel.posy > SBC.Player1.posy:
                                if vessel.posy - 1 >= 0:
                                    if self.board[vessel.posx][vessel.posy - 1] == 0:
                                        self.board[vessel.posx][vessel.posy] = 0
                                        vessel.posy -= 1
                                        self.board[vessel.posx][vessel.posy] = vessel
                                        item.x -= 50
                                        item.move_self(item.x, item.y)
                                    elif self.board[vessel.posx][vessel.posy - 1].type == 'Wall':
                                        if vessel.posx < SBC.Player1.posx and self.board[vessel.posx + 1][vessel.posy] == 0:
                                            self.board[vessel.posx][vessel.posy] = 0
                                            vessel.posx += 1
                                            self.board[vessel.posx][vessel.posy] = vessel
                                            item.y += 50
                                            item.move_self(item.x, item.y)
                                        elif vessel.posy > SBC.Player1.posy and self.board[vessel.posx - 1][vessel.posy] == 0:
                                            self.board[vessel.posx][vessel.posy] = 0
                                            vessel.posx -= 1
                                            self.board[vessel.posx][vessel.posy] = vessel
                                            item.y -= 50
                                            item.move_self(item.x, item.y)
                                else:
                                    print('Waka waka')
                        else:
                            print('Oink')

    def fight(self, object1, object2):
        if object1.posx - 1 == object2.posx and object1.posy == object2.posy:
            dmg = object1.stg - object2.armor
            pc_dmg = object2.stg - object1.armor
            object1.hp -= pc_dmg
            object2.hp -= dmg
            if object1.hp <= 0:
                object1.is_dead = True
                object1.drop_loot()
                self.board[object1.posx][object1.posy] = object1.loot
                for item in self.list_of_objects:
                    if item.object == object1:
                        item.add_object(object1.loot)
                        print(item.object)
                        item.change_image('smallbag.png')
            if object2.hp <= 0:
                object2.is_dead = True
            print(object1.hp)
            print(object2.hp)
        elif object1.posx + 1 == object2.posx and object1.posy == object2.posy:
            dmg = object1.stg - object2.armor
            pc_dmg = object2.stg - object1.armor
            object1.hp -= pc_dmg
            object2.hp -= dmg
            if object1.hp <= 0:
                object1.is_dead = True
                object1.drop_loot()
                self.board[object1.posx][object1.posy] = object1.loot
                for item in self.list_of_objects:
                    if item.object == object1:
                        item.add_object(object1.loot)
                        print(item.object)
                        item.change_image('smallbag.png')
            if object2.hp <= 0:
                object2.is_dead = True
            print(self.board)
            print(object1.hp)
            print(object2.hp)
        elif object1.posx == object2.posx and object1.posy + 1 == object2.posy:
            dmg = object1.stg - object2.armor
            pc_dmg = object2.stg - object1.armor
            object1.hp -= pc_dmg
            object2.hp -= dmg
            if object1.hp <= 0:
                object1.is_dead = True
                object1.drop_loot()
                self.board[object1.posx][object1.posy] = object1.loot
                for item in self.list_of_objects:
                    if item.object == object1:
                        item.add_object(object1.loot)
                        item.change_image('smallbag.png')
            if object2.hp <= 0:
                object2.is_dead = True
            print(object1.hp)
            print(object2.hp)
        elif object1.posx == object2.posx and object1.posy - 1 == object2.posy:
            dmg = object1.stg - object2.armor
            pc_dmg = object2.stg - object1.armor
            object1.hp -= pc_dmg
            object2.hp -= dmg
            if object1.hp <= 0:
                object1.is_dead = True
                object1.drop_loot()
                self.board[object1.posx][object1.posy] = object1.loot
                for item in self.list_of_objects:
                    if item.object == object1:
                        item.add_object(object1.loot)
                        item.change_image('smallbag.png')
            if object2.hp <= 0:
                object2.is_dead = True
            print(object1.hp)
            print(object2.hp)

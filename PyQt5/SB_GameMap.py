import SB_WidgetsClass as SBWC
import SB_Characters as SBC
import SB_SkillTrees as SBST
import SB_Objects as SBOB


class GameMap:
    def __init__(self):
        # Create an empty board
        self.board = [[0 for x in range(0, 10)] for x in range(0, 10)]
        self.list_of_objects = []

        ''' As the game board is using PyQt Labels to display objects, after any of the objects gets destroyed
        we want to recycle it's label so as to not to waste memory on creating new labels for every new objects'''
        self.removed_list = []

        self.player_casting_spell = False

    def create_map(self, window):
        # X and Y on the board
        num_of_x = 0
        num_of_y = 0
        # X and Y for PyQt Labels
        xpos = 175
        ypos = 50
        for x in self.board:
            for y in x:
                #floor = SBWC.LabelObject('floortile.png', window_name, xpos, ypos, '')
                #floor.new_label.hide()
                if y != 0:
                    #Check if there are any labels left after destroyed objects
                    if len(self.removed_list) == 0:

                        if self.board[num_of_x][num_of_y].type == 'Creature':
                            print(self.board[num_of_x][num_of_y].game_image)
                            object_on_map = SBWC.LabelObject(window, self.board[num_of_x][num_of_y].game_image,  xpos, ypos, self.board[num_of_x][num_of_y].name)
                            object_on_map.attach_object(self.board[num_of_x][num_of_y])
                            self.list_of_objects.append(object_on_map)
                        elif self.board[num_of_x][num_of_y].type == 'Wall':
                            object_on_map = SBWC.LabelObject(window, self.board[num_of_x][num_of_y].game_image, xpos, ypos, self.board[num_of_x][num_of_y].name)
                            object_on_map.attach_object(self.board[num_of_x][num_of_y])
                            self.list_of_objects.append(object_on_map)
                    else:
                        if self.board[num_of_x][num_of_y].type == 'Creature':
                            self.removed_list[0].add_object(self.board[num_of_x][num_of_y])
                            self.removed_list[0].change_image(self.board[num_of_x][num_of_y].game_image)
                            self.removed_list[0].change_id(self.board[num_of_x][num_of_y].name)
                            self.removed_list[0].move_self(xpos, ypos)
                            self.list_of_objects.append(self.removed_list[0])
                            self.removed_list.remove(self.removed_list[0])
                xpos += 50
                num_of_y += 1
            num_of_x += 1
            num_of_y = 0
            ypos += 50
            xpos = 175
        print(self.board)

    def move_player(self, direction, player):
      try:
        if direction == 'Up':
            if player.cordx - 1 < 0:
                pass
            elif self.board[player.cordx - 1][player.cordy] == 0:
                self.board[player.cordx][player.cordy] = 0
                player.cordx -= 1
                self.board[player.cordx][player.cordy] = player
                for label in self.list_of_objects:
                    if label.id == player.name:
                        label.cordy -= 50
                        label.new_label.move(label.cordx, label.cordy)
            elif self.board[player.cordx - 1][player.cordy] != 0:
                for item in self.list_of_objects:
                    print(item)
                    if item.object_data.type == 'Container':
                        self.board[player.cordx][player.cordy] = 0
                        player.cordx -= 1
                        player.pick_up_loot(item.object_data.loot_list)
                        self.board[player.cordx][player.cordy] = player
                        item.change_image('')
                        item.attach_object('')
                        self.list_of_objects.remove(item)
                        self.removed_list.append(item)
                        for label in self.list_of_objects:
                            if label.id == player.name:
                                label.cordy -= 50
                                label.new_label.move(item.cordx, item.cordy)
                    else:
                        pass
            else:
                pass
        if direction == 'Down':
            if player.cordx + 1 > 9:
                pass
            elif self.board[player.cordx + 1][player.cordy] == 0:
                self.board[player.cordx][player.cordy] = 0
                player.cordx += 1
                self.board[player.cordx][player.cordy] = player
                for label in self.list_of_objects:
                    if label.id == player.name:
                        label.cordy += 50
                        label.new_label.move(label.cordx, label.cordy)
            elif self.board[player.cordx + 1][player.cordy] != 0:
                for item in self.list_of_objects:
                    if item.object_data.type == 'Container':
                        self.board[player.cordx][player.cordy] = 0
                        player.cordx += 1
                        player.pick_up_loot(item.object_data.loot_list)
                        self.board[player.cordx][player.cordy] = player
                        item.change_image('')
                        item.attach_object('')
                        self.list_of_objects.remove(item)
                        self.removed_list.append(item)
                        for label in self.list_of_objects:
                            if label.id == player.name:
                                label.cordy -= 50
                                label.new_label.move(item.cordx, item.cordy)
            else:
                pass
        if direction == 'Left':
            if player.cordy - 1 < 0:
                pass
            elif self.board[player.cordx][player.cordy - 1] == 0:
                self.board[player.cordx][player.cordy] = 0
                player.cordy -= 1
                self.board[player.cordx][player.cordy] = player
                for label in self.list_of_objects:
                    if label.id == player.name:
                        label.cordx -= 50
                        label.new_label.move(label.cordx, label.cordy)
            elif self.board[player.cordx][player.cordy - 1] != 0:
                for item in self.list_of_objects:
                    if item.object_data.type == 'Container':
                        self.board[player.cordx][player.cordy] = 0
                        player.cordy -= 1
                        player.pick_up_loot(item.object_data.loot_list)
                        self.board[player.cordx][player.cordy] = player
                        item.change_image('')
                        item.attach_object('')
                        self.list_of_objects.remove(item)
                        self.removed_list.append(item)
                        for label in self.list_of_objects:
                            if label.id == player.name:
                                label.cordy -= 50
                                label.new_label.move(item.x, item.y)
            else:
                pass
        if direction == 'Right':
            if player.cordy + 1 > 9:
                pass
            elif self.board[player.cordx][player.cordy + 1] == 0:
                self.board[player.cordx][player.cordy] = 0
                player.cordy += 1
                self.board[player.cordx][player.cordy] = player
                for label in self.list_of_objects:
                    if label.id == player.name:
                        label.cordx += 50
                        label.new_label.move(label.cordx, label.cordy)
            elif self.board[player.cordx][player.cordy + 1] != 0:
                for item in self.list_of_objects:
                    if item.object_data.type == 'Container':
                        self.board[player.cordx][player.cordy] = 0
                        player.cordy += 1
                        player.pick_up_loot(item.object_data.loot_list)
                        self.board[player.cordx][player.cordy] = player
                        item.change_image('')
                        item.attach_object('')
                        self.list_of_objects.remove(item)
                        self.removed_list.append(item)
                        for label in self.list_of_objects:
                            if label.id == player.name:
                                label.cordx += 50
                                label.new_label.move(item.cordx, item.cordy)
            else:
                pass

      except Exception as e:
          print(e)

    def move_enemy(self):
      try:
        for label in self.list_of_objects:
            if label.object_data.type == "Creature" and isinstance(label.object_data, SBC.Monster):
                vessel = label.object_data
                if vessel.health > 0:
                    if vessel.cordx < 9 and self.board[vessel.cordx + 1][vessel.cordy] != 0 and isinstance(self.board[vessel.cordx + 1][vessel.cordy], SBC.Player):
                        for player in SBC.list_of_players_on_the_map:
                            if vessel.cordx < 9 and self.board[vessel.cordx + 1][vessel.cordy].name == player.name:
                                self.fight(vessel, player)
                    if vessel.cordx > 0 and self.board[vessel.cordx - 1][vessel.cordy] != 0 and isinstance(self.board[vessel.cordx - 1][vessel.cordy], SBC.Player):
                        for player in SBC.list_of_players_on_the_map:
                            if vessel.cordx > 0 and self.board[vessel.cordx - 1][vessel.cordy].name == player.name:
                                self.fight(vessel, player)
                    if vessel.cordy < 9 and self.board[vessel.cordx][vessel.cordy + 1] != 0 and isinstance(self.board[vessel.cordx][vessel.cordy + 1], SBC.Player):
                        for player in SBC.list_of_players_on_the_map:
                            if vessel.cordy < 9 and self.board[vessel.cordx][vessel.cordy + 1].name == player.name:
                                self.fight(vessel, player)
                    if vessel.cordy > 0 and self.board[vessel.cordx][vessel.cordy - 1] != 0 and isinstance(self.board[vessel.cordx][vessel.cordy - 1], SBC.Player):
                        for player in SBC.list_of_players_on_the_map:
                            if vessel.cordy > 0 and self.board[vessel.cordx][vessel.cordy - 1].name == player.name:
                                self.fight(vessel, player)
                    target = SBC.list_of_players_on_the_map[0]
                    initial_x = vessel.cordx
                    initial_y = vessel.cordy
                    initial_label_x = label.cordx
                    initial_label_y = label.cordy

                    visited = []

                    reached_the_goal = False

                    while reached_the_goal == False:
                        print('Goobson')
                        print(vessel.pathfinding)

                        if vessel.cordx < 9 and self.board[vessel.cordx + 1][vessel.cordy] == 0 and vessel.cordx \
                            < target.cordx and (vessel.cordx + 1, vessel.cordy) not in visited and (vessel.cordx + 1, vessel.cordy) not in vessel.pathfinding \
                                or vessel.cordx < 9 and self.board[vessel.cordx + 1][vessel.cordy] == target\
                                and (vessel.cordx, vessel.cordy) not in visited:
                            vessel.cordx += 1
                            if self.board[vessel.cordx][vessel.cordy] == target:
                                reached_the_goal = True
                                break
                            label.cordy += 50
                            vessel.pathfinding.append((vessel.cordx, vessel.cordy, label.cordx, label.cordy))
                        elif vessel.cordx > 0 and self.board[vessel.cordx - 1][vessel.cordy] == 0 and vessel.cordx \
                            > target.cordx and (vessel.cordx - 1, vessel.cordy) not in visited and (vessel.cordx - 1, vessel.cordy) not in vessel.pathfinding \
                               or vessel.cordx > 0 and self.board[vessel.cordx - 1][vessel.cordy] == target\
                               and (vessel.cordx, vessel.cordy) not in visited:
                            vessel.cordx -= 1
                            if self.board[vessel.cordx][vessel.cordy] == target:
                                reached_the_goal = True
                                break
                            label.cordy -= 50
                            vessel.pathfinding.append((vessel.cordx, vessel.cordy, label.cordx, label.cordy))
                        elif vessel.cordy > 0 and self.board[vessel.cordx][vessel.cordy - 1] == 0 and vessel.cordy \
                            > target.cordy and (vessel.cordx, vessel.cordy - 1) not in visited and (vessel.cordx, vessel.cordy - 1) not in vessel.pathfinding \
                                or vessel.cordy > 0 and self.board[vessel.cordx][vessel.cordy - 1] == target\
                               and (vessel.cordx, vessel.cordy - 1) not in visited:
                            vessel.cordy -= 1
                            if self.board[vessel.cordx][vessel.cordy] == target:
                                reached_the_goal = True
                                break
                            label.cordx -= 50
                            vessel.pathfinding.append((vessel.cordx, vessel.cordy, label.cordx, label.cordy))
                        elif vessel.cordy < 9 and self.board[vessel.cordx][vessel.cordy + 1] == 0 and vessel.cordy < \
                            target.cordy and (vessel.cordx, vessel.cordy + 1) not in visited and (vessel.cordx, vessel.cordy + 1) not in vessel.pathfinding \
                            or vessel.cordy < 9 and self.board[vessel.cordx][vessel.cordy + 1] == target\
                                and (vessel.cordx, vessel.cordy + 1) not in visited:
                            vessel.cordy += 1
                            if self.board[vessel.cordx][vessel.cordy] == target:
                                reached_the_goal = True
                                break
                            label.cordx += 50
                            vessel.pathfinding.append((vessel.cordx, vessel.cordy, label.cordx, label.cordy))
                        elif vessel.cordy > 0 and self.board[vessel.cordx][vessel.cordy - 1] == 0 \
                            and (vessel.cordx, vessel.cordy - 1) not in visited and (vessel.cordx, vessel.cordy - 1) not in vessel.pathfinding\
                                or vessel.cordy > 0 and self.board[vessel.cordx][vessel.cordy - 1] == target\
                                and (vessel.cordx, vessel.cordy - 1) not in visited:
                            vessel.cordy -= 1
                            if self.board[vessel.cordx][vessel.cordy] == target:
                                reached_the_goal = True
                                break
                            label.cordx -= 50
                            vessel.pathfinding.append((vessel.cordx, vessel.cordy, label.cordx, label.cordy))
                        elif vessel.cordy < 9 and self.board[vessel.cordx][vessel.cordy + 1] == 0 \
                            and (vessel.cordx, vessel.cordy + 1) not in visited and (vessel.cordx, vessel.cordy + 1) not in vessel.pathfinding\
                                or vessel.cordy < 9 and self.board[vessel.cordx][vessel.cordy + 1] == target\
                                and (vessel.cordx, vessel.cordy + 1) not in visited:
                            vessel.cordy += 1
                            if self.board[vessel.cordx][vessel.cordy] == target:
                                reached_the_goal = True
                                break
                            label.cordx += 50
                            vessel.pathfinding.append((vessel.cordx, vessel.cordy, label.cordx, label.cordy))
                        elif vessel.cordx > 0 and self.board[vessel.cordx - 1][vessel.cordy] == 0 \
                            and (vessel.cordx - 1, vessel.cordy) not in visited and (vessel.cordx - 1, vessel.cordy) not in vessel.pathfinding \
                                or vessel.cordx > 0 and self.board[vessel.cordx - 1][vessel.cordy] == target\
                                and (vessel.cordx - 1, vessel.cordy) not in visited:
                            vessel.cordx -= 1

                            if self.board[vessel.cordx][vessel.cordy] == target:
                                reached_the_goal = True
                                break
                            label.cordy -= 50
                            vessel.pathfinding.append((vessel.cordx, vessel.cordy, label.cordx, label.cordy))
                        elif vessel.cordx < 9 and self.board[vessel.cordx + 1][vessel.cordy] == 0 \
                            and (vessel.cordx + 1, vessel.cordy) not in visited and (vessel.cordx + 1, vessel.cordy) not in vessel.pathfinding\
                                or vessel.cordx < 9 and self.board[vessel.cordx + 1][vessel.cordy] == target\
                                and (vessel.cordx + 1, vessel.cordy) not in visited:
                            vessel.cordx += 1
                            if self.board[vessel.cordx][vessel.cordy] == target:
                                reached_the_goal = True
                                break
                            label.cordy += 50
                            vessel.pathfinding.append((vessel.cordx, vessel.cordy, label.cordx, label.cordy))
                        elif len(vessel.pathfinding) == 0:
                            print('Kwik')

                            print(self.board)
                            vessel.cordx = initial_x
                            vessel.cordy = initial_y
                        else:
                            print('Kwak')
                            vessel.cordx, vessel.cordy, x, y = vessel.pathfinding[-1]
                            visited.append(vessel.pathfinding[-1])
                            vessel.pathfinding.remove((vessel.cordx, vessel.cordy, x, y))

                    if reached_the_goal == True:
                        vessel.cordx, vessel.cordy = initial_x, initial_y
                        if len(vessel.pathfinding) > 0 and vessel.pathfinding[0] != target:
                            self.board[vessel.cordx][vessel.cordy] = 0
                            vessel.cordx, vessel.cordy, label.cordx, label.cordy = vessel.pathfinding[0]
                            print(vessel.cordx, vessel.cordy, label.cordx, label.cordy)
                            self.board[vessel.cordx][vessel.cordy] = vessel
                            label.new_label.move(label.cordx, label.cordy)
                            vessel.pathfinding = []

                    print(self.board)


      except Exception as e:
             print(e)

    def fight(self, object1, object2):
        dmg = object1.strength - object2.armor
        pc_dmg = object2.strength - object1.armor
        if object1.cordx - 1 == object2.cordx and object1.cordy == object2.cordy:
            object1.health -= pc_dmg
            object2.health -= dmg
            if object1.health <= 0:
                object1.is_dead = True
                object1.drop_loot()
                self.board[object1.cordx][object1.cordy] = object1.loot
                for item in self.list_of_objects:
                    if item.object == object1:
                        item.add_object(object1.loot)
                        item.change_image('smallbag.png')
            if object2.health <= 0:
                object2.is_dead = True
        elif object1.cordx + 1 == object2.cordx and object1.cordy == object2.cordy:
            object1.health -= pc_dmg
            object2.health -= dmg
            if object1.health <= 0:
                object1.is_dead = True
                object1.drop_loot()
                self.board[object1.cordx][object1.cordy] = object1.loot
                for item in self.list_of_objects:
                    if item.object == object1:
                        item.add_object(object1.loot)
                        item.change_image('smallbag.png')
            if object2.health <= 0:
                object2.is_dead = True
        elif object1.cordx == object2.cordx and object1.cordy + 1 == object2.cordy:
            object1.health -= pc_dmg
            object2.health -= dmg
            if object1.health <= 0:
                object1.is_dead = True
                object1.drop_loot()
                self.board[object1.cordx][object1.cordy] = object1.loot
                for item in self.list_of_objects:
                    if item.object == object1:
                        item.add_object(object1.loot)
                        item.change_image('smallbag.png')
            if object2.health <= 0:
                object2.is_dead = True
        elif object1.cordx == object2.cordx and object1.cordy - 1 == object2.cordy:
            object1.health -= pc_dmg
            object2.health -= dmg
            if object1.health <= 0:
                object1.is_dead = True
                object1.drop_loot()
                self.board[object1.cordx][object1.cordy] = object1.loot
                for item in self.list_of_objects:
                    if item.object == object1:
                        item.add_object(object1.loot)
                        item.change_image('smallbag.png')
            if object2.health <= 0:
                object2.is_dead = True

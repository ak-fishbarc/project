import sys
import socket
import threading
import select
import asyncio
import pickle
import re
import random as rnd
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import SB_GameMap as SBGM
import SB_WidgetsClass as SBWC
import SB_Characters as SBC
import SB_Professions as SBP
import SB_SkillTrees as SBST
import SB_Objects as SBOB
import SB_Inventory as SBI
import SB_ESCOptions as SBESC


class MenuWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Spellbook v.0.0.1"
        self.height = 1240
        self.width = 960

        '''Sub-windows code: '''

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        self.start_menu = QMdiSubWindow(self)
        self.start_menu.hide()

        self.create_character_win = QMdiSubWindow(self)
        self.create_character_win.hide()

        self.game_display_win = QMdiSubWindow(self)
        self.game_display_win.hide()

        self.escape_options = SBESC.Options(self)

        self.network_game = QMdiSubWindow(self)
        self.network_game.hide()

        self.list_of_maps = []
        self.game_board = None
        self.game_running = False
        '''Start main window: '''

        self.initUI()

    #############################################################################
    ###################  Window initialization section  #########################
    #############################################################################

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(400, 100, self.height, self.width)

        '''Start menu window and show main window: '''

        self.initStartMenu()

        self.show()

    def initStartMenu(self):
        self.start_menu.setWindowTitle("Menu")
        self.start_menu.setGeometry(0, 0, self.height, self.width)

        new_game_but = SBWC.ButtonObject("New Game", self.start_menu, 350, 150, "new_game_button")
        new_game_but.activate_event(self.start_character_creation)

        load_game_but = SBWC.ButtonObject("Load Game", self.start_menu, 350, 200, "load_game_but")
        load_game_but.activate_event(self.load_game_options)

        multiplayer_but = SBWC.ButtonObject("Multiplayer", self.start_menu, 350, 250, "multiplayer_but")
        #multiplayer_but.activate_event(self.multiplayer_game)

        self.start_menu.show()

    def initCharacterCreation(self):
        def change_player_name():
            SBC.New_Player.name = str(enter_player_name.text_box.text())
            display_statistics.new_label.setText(player_stats())

        def change_class():
            for profession in SBP.list_of_professions:
                if str(choose_class_box.new_box.currentText()) == profession.name:
                    SBC.New_Player.profession = profession
                    SBC.New_Player.set_stats()
            display_statistics.new_label.setText(player_stats())
            display_skills(self.create_character_win)

        # Lists to store skill labels
        list_of_barbarian = []
        list_of_wizard = []

        def display_skills(window):
            def create_labels(profession_name, list_name):
                x = 600
                y = 200
                for item in SBST.list_of_trees:
                    if item.name == profession_name:
                        for skill in item.tier1:
                            skill_label = SBWC.LabelObject(window, str(skill.skill_icon), x, y, skill.name)
                            skill_name_label = SBWC.LabelObject(window, "", x, y - 25, skill.name)
                            skill_name_label.new_label.setText(str(skill.name))
                            skill_name_label.new_label.resize(90, 25)
                            list_name.append(skill_label)
                            list_name.append(skill_name_label)
                            x += 50
                        x = 500
                        y = 280
                        for skill in item.tier2:
                            skill_label = SBWC.LabelObject(window, str(skill.skill_icon), x, y, skill.name)
                            skill_name_label = SBWC.LabelObject(window, "", x, y - 25, skill.name)
                            skill_name_label.new_label.setText(str(skill.name))
                            skill_name_label.new_label.resize(90, 25)
                            list_name.append(skill_label)
                            list_name.append(skill_name_label)
                            x += 50
                        x = 450
                        y = 330
                        for skill in item.tier3:
                            skill_label = SBWC.LabelObject(window, str(skill.skill_icon), x, y, skill.name)
                            skill_name_label = SBWC.LabelObject(window, "", x, y - 25, skill.name)
                            skill_name_label.new_label.setText(str(skill.name))
                            skill_name_label.new_label.resize(90, 25)
                            list_name.append(skill_label)
                            list_name.append(skill_name_label)
                            x += 50
                        x = 400
                        y = 380
                        for skill in item.tier4:
                            skill_label = SBWC.LabelObject(window, str(skill.skill_icon), x, y, skill.name)
                            skill_name_label = SBWC.LabelObject(window, "", x, y - 25, skill.name)
                            skill_name_label.new_label.setText(str(skill.name))
                            skill_name_label.new_label.resize(90, 25)
                            list_name.append(skill_label)
                            list_name.append(skill_name_label)
                            x += 50
                        x = 350
                        y = 430
                        for skill in item.tier5:
                            skill_label = SBWC.LabelObject(window, str(skill.skill_icon), x, y, skill.name)
                            skill_name_label = SBWC.LabelObject(window, "", x - 15, y - 25, skill.name)
                            skill_name_label.new_label.setText(str(skill.name))
                            skill_name_label.new_label.resize(90, 25)
                            list_name.append(skill_label)
                            list_name.append(skill_name_label)
                            x += 50
            # Code to hide and show labels
            for item in SBST.list_of_trees:
                if item.name == SBC.New_Player.profession.name:
                    if item.name == 'Barbarian' and len(list_of_barbarian) == 0:
                        if len(list_of_wizard) > 0:
                            for label in list_of_wizard:
                                label.new_label.hide()
                        create_labels('Barbarian', list_of_barbarian)
                    elif item.name == 'Wizard' and len(list_of_wizard) == 0:
                        if len(list_of_barbarian) > 0:
                            for label in list_of_barbarian:
                                label.new_label.hide()
                        create_labels('Wizard', list_of_wizard)
                        for label in list_of_wizard:
                            label.new_label.show()
                    elif item.name == 'Barbarian' and len(list_of_barbarian) > 0:
                        if len(list_of_wizard) > 0:
                            for label in list_of_wizard:
                                label.new_label.hide()
                        for label in list_of_barbarian:
                            label.new_label.show()
                    elif item.name == 'Wizard' and len(list_of_wizard) > 0:
                        if len(list_of_barbarian) > 0:
                            for label in list_of_barbarian:
                                label.new_label.hide()
                        for label in list_of_wizard:
                            label.new_label.show()

        def player_stats():
            player_stats = "Name: {} \n" \
                     "Class: {} \n" \
                     "Level: {} \n" \
                     "Strength: {} \n" \
                     "Dexterity: {} \n" \
                     "Endurance: {} \n" \
                     "Intelligence: {} \n" \
                     "Wisdom: {} \n" \
                     "Health: {} \n" \
                     "Armor: {}".format(SBC.New_Player.name, SBC.New_Player.profession.name,
                                        SBC.New_Player.level, SBC.New_Player.strength,
                                        SBC.New_Player.dexterity, SBC.New_Player.endurance,
                                        SBC.New_Player.intelligence, SBC.New_Player.wisdom,
                                        SBC.New_Player.health, SBC.New_Player.armor)
            return player_stats

        self.create_character_win.setWindowTitle('Create Character')
        self.create_character_win.setGeometry(0, 0, self.height, self.width)

        enter_player_name = SBWC.TextInput(self.create_character_win, 50, 100,
                                           100, 25)
        enter_player_name.text_box.returnPressed.connect(change_player_name)

        choose_class_box = SBWC.ComboxObject(self.create_character_win, 50, 150, *SBP.list_of_professions)
        choose_class_box.new_box.activated.connect(change_class)

        show_player_picture = SBWC.LabelObject( self.create_character_win, os.getcwd() + "barbarian.png",
                                               320, 200, "")
        show_player_picture.new_label.resize(150, 150)

        display_statistics = SBWC.LabelObject(self.create_character_win, "", 200, 200, "")
        display_statistics.new_label.resize(200, 150)
        display_statistics.new_label.setText(player_stats())
        display_skills(self.create_character_win)

        start_game_but = SBWC.ButtonObject("Start Game", self.create_character_win, 600, 400,
                                           "start_game_but")
        start_game_but.new_button.clicked.connect(self.start_game_display)

        self.create_character_win.show()

    ################################################################################
    ############################  Game Mode Functions  #############################
    ################################################################################
    def initLoadedGame(self, *objects):
      try:

          player_characters = None
          monsters = None
          walls = None
          length = len(objects) - 1
          if length >= 0:
              player_characters = objects[0]
          if length >= 1:
              monsters = objects[1]
          if length >= 2:
              walls = objects[2]
          print(walls)
          print(player_characters)
          self.game_board = SBGM.GameMap()
          self.list_of_maps.append(self.game_board)

          for player in player_characters:
              player.show_inventory_win = SBI.Inventory(self.game_display_win, player)
              player.show_inventory_win.hide_inventory()
              self.game_board.board[player.cordx][player.cordy] = player
              self.game_board.list_of_objects.append(player)

          if walls:
              for wall in walls:
                  print(wall.pattern)
                  if wall.pattern == 1:
                      print('Here')
                      print(wall.tiles)
                      print(wall.cordy)
                      print(wall.cordx)
                      if wall.cordy <= 4:
                          print('HEre')
                          self.game_board.board[wall.cordx][wall.cordy] = wall
                          while wall.tiles > 0:
                              wall.tiles -= 1
                              wall.cordy += 1
                              print('Eek')
                              self.game_board.board[wall.cordx][wall.cordy] = wall
                      elif wall.cordy >= 5:
                          print('here')
                          self.game_board.board[wall.cordx][wall.cordy] = wall
                          while wall.tiles > 0:
                              wall.tiles -= 1
                              wall.cordy -= 1
                              self.game_board.board[wall.cordx][wall.cordy] = wall
                  if wall.pattern == 2:
                      print('ERe')
                      # Vertical wall, can't be too close to top or bottom of the board
                      if wall.cordx <= 4:
                          self.game_board.board[wall.cordx][wall.cordy] = wall
                          while wall.tiles > 0:
                              wall.tiles -= 1
                              wall.cordx -= 1
                              self.game_board.board[wall.cordx][wall.cordy] = wall
                      elif wall.cordx >= 5:
                          self.game_board.board[wall.cordx][wall.cordy] = wall
                          while wall.tiles > 0:
                              wall.tiles -= 1
                              wall.cordx += 1
                              self.game_board.board[wall.cordx][wall.cordy] = wall
                  if wall.pattern == 3:
                      # House patter, check the size of the map and based on that find position
                      # Start from the front
                      left_front_tiles = 1
                      while left_front_tiles >= 0:
                          left_front_tiles -= 1
                          wall.tiles -= 1
                          wall.cordy -= 1
                          self.game_board.board[wall.cordx][wall.cordy] = wall
                      left_side_tiles = 2
                      while left_side_tiles >= 0:
                          left_side_tiles -= 1
                          wall.cordx -= 1
                          self.game_board.board[wall.cordx][wall.cordy] = wall
                      back_tiles = 3
                      while back_tiles >= 0:
                          back_tiles -= 1
                          wall.cordy += 1
                          self.game_board.board[wall.cordx][wall.cordy] = wall
                      left_side_tiles = 2
                      while left_side_tiles >= 0:
                          left_side_tiles -= 1
                          wall.cordx += 1
                          self.game_board.board[wall.cordx][wall.cordy] = wall
                      left_front_tiles = 0
                      while left_front_tiles >= 0:
                          left_front_tiles -= 1
                          wall.cordy -= 1
                          self.game_board.board[wall.cordx][wall.cordy] = wall

          monster_spawner = []
          if monsters:
              for creature in monsters:
                  self.game_board.board[creature.cordx][creature.cordy] = creature

          self.game_board.create_map(self.game_display_win)

          self.game_display_win.setWindowTitle('Game Display')
          self.game_display_win.setGeometry(0, 0, self.height, self.width)
          self.game_display_win.setWindowFlags(self.game_display_win.windowFlags() | Qt.FramelessWindowHint)

          self.game_display_win.hide()
          self.game_running = True

          self.game_display_win.show()
      except Exception as e:
          print(e)

    def load_game_options(self):
        self.start_menu.hide()
        self.escape_options.load_game_to_gamemap()
        self.escape_options.show_options()

    def start_character_creation(self):
        self.start_menu.hide()
        self.initCharacterCreation()

    def start_game_display(self):
        self.create_character_win.hide()
        self.initGameDisplay(SBC.list_of_players, SBC.list_of_monsters, SBOB.list_of_walls)

    def initGameDisplay(self, *objects):
      try:
        player_characters = None
        monsters = None
        walls = None
        length = len(objects) - 1
        if length >= 0:
            player_characters = objects[0]
        if length >= 1:
            monsters = objects[1]
        if length >= 2:
            walls = objects[2]

        self.game_board = SBGM.GameMap()
        self.list_of_maps.append(self.game_board)
        for player in player_characters:
            player.show_inventory_win = SBI.Inventory(self.game_display_win, player)
            player.show_inventory_win.hide_inventory()
            player.cordx = 9
            player.cordy = 4
            self.game_board.board[player.cordx][player.cordy] = player
            SBC.list_of_players_on_the_map.append(player)

        if walls:
            for wall in walls:
                pattern = rnd.randint(1, 3)
                how_many_tiles = rnd.randint(1, 4)
                wall.pattern = pattern
                wall.tiles = how_many_tiles
                if pattern == 1:
                    # Horizontal wall, can't be too close to side edges of the board
                        wall.cordx = rnd.randint(0, 9)
                        wall.cordy = rnd.randint(4, 5)
                        # How many tiles should the wall take
                        if wall.cordy == 4:
                            self.game_board.board[wall.cordx][wall.cordy] = wall
                            while how_many_tiles > 0:
                                how_many_tiles -= 1
                                wall.cordy -= 1
                                self.game_board.board[wall.cordx][wall.cordy] = wall
                        elif wall.cordy == 5:
                            self.game_board.board[wall.cordx][wall.cordy] = wall
                            while how_many_tiles > 0:
                                how_many_tiles -= 1
                                wall.cordy += 1
                                self.game_board.board[wall.cordx][wall.cordy] = wall
                if pattern == 2:
                    # Vertical wall, can't be too close to top or bottom of the board
                    wall.cordx = rnd.randint(4, 5)
                    wall.cordy = rnd.randint(0, 9)
                    if wall.cordx == 4:
                        self.game_board.board[wall.cordx][wall.cordy] = wall
                        SBOB.list_of_walls_on_the_map.append(wall)
                        while how_many_tiles > 0:
                            how_many_tiles -= 1
                            wall.cordx += 1
                            self.game_board.board[wall.cordx][wall.cordy] = wall
                            SBOB.list_of_walls_on_the_map.append(wall)
                    elif wall.cordx == 5:
                        self.game_board.board[wall.cordx][wall.cordy] = wall
                        SBOB.list_of_walls_on_the_map.append(wall)
                        while how_many_tiles > 0:
                            how_many_tiles -= 1
                            wall.cordx -= 1
                            self.game_board.board[wall.cordx][wall.cordy] = wall
                            SBOB.list_of_walls_on_the_map.append(wall)
                if pattern == 3:
                        # House pattern, check the size of the map and based on that find position
                        wall.cordx = rnd.randint(4, 5)
                        wall.cordy = rnd.randint(4, 5)
                        # Start from the front
                        left_front_tiles = 1
                        while left_front_tiles >= 0:
                            left_front_tiles -= 1
                            wall.cordy -= 1
                            self.game_board.board[wall.cordx][wall.cordy] = wall
                            SBOB.list_of_walls_on_the_map.append(wall)
                        left_side_tiles = 2
                        while left_side_tiles >= 0:
                            left_side_tiles -= 1
                            wall.cordx -= 1
                            self.game_board.board[wall.cordx][wall.cordy] = wall
                            SBOB.list_of_walls_on_the_map.append(wall)
                        back_tiles = 3
                        while back_tiles >= 0:
                            back_tiles -= 1
                            wall.cordy += 1
                            self.game_board.board[wall.cordx][wall.cordy] = wall
                            SBOB.list_of_walls_on_the_map.append(wall)
                        left_side_tiles = 2
                        while left_side_tiles >= 0:
                            left_side_tiles -= 1
                            wall.cordx += 1
                            self.game_board.board[wall.cordx][wall.cordy] = wall
                            SBOB.list_of_walls_on_the_map.append(wall)
                        left_front_tiles = 0
                        while left_front_tiles >= 0:
                            left_front_tiles -= 1
                            wall.cordy -= 1
                            self.game_board.board[wall.cordx][wall.cordy] = wall
                            SBOB.list_of_walls_on_the_map.append(wall)

        monster_spawner = []
        if monsters:
            for creature in monsters:
                if creature.name == 'Goblin':
                    number_of_creatures = rnd.randint(1, 3)
                    while number_of_creatures > 0:
                        number_of_creatures -= 1
                        new_id_tag = creature.id_tag
                        new_id_tag += 1
                        new_creature = SBC.Monster("Goblin", 1, SBP.Barbarian, 'goblin.png', new_id_tag, 0, 0)
                        SBC.list_of_monster_on_the_map.append(new_creature)
                        monster_spawner.append(new_creature)
        for creature in monster_spawner:
            creature.cordx = rnd.randint(0, 9)
            creature.cordy = rnd.randint(0, 9)
            if self.game_board.board[creature.cordx][creature.cordy] == 0:
                self.game_board.board[creature.cordx][creature.cordy] = creature
                monster_spawner.remove(creature)
            else:
                while self.game_board.board[creature.cordx][creature.cordy] != 0:
                    creature.cordx = rnd.randint(0, 9)
                    creature.cordy = rnd.randint(0, 9)
                    if self.game_board.board[creature.cordx][creature.cordy] == 0:
                        self.game_board.board[creature.cordx][creature.cordy] = creature
                        monster_spawner.remove(creature)
                        break

        self.game_display_win.setWindowTitle('Game Display')
        self.game_display_win.setGeometry(0, 0, self.height, self.width)
        self.game_display_win.setWindowFlags(self.game_display_win.windowFlags() | Qt.FramelessWindowHint)

        self.game_board.create_map(self.game_display_win)

        self.game_running = True

        self.game_display_win.show()
      except Exception as e:
          print(e)


    def keyPressEvent(self, event):
        player = SBC.New_Player
        if self.escape_options.game_loaded == True:
            self.escape_options.game_loaded = False
            self.initLoadedGame(SBC.list_of_players_on_the_map, SBC.list_of_monster_on_the_map, SBOB.list_of_walls_on_the_map)
        if event.key() == Qt.Key_I:
            SBC.New_Player.show_inventory_win.open_inventory()
        if self.game_running:
            if event.key() == Qt.Key_Escape:
                if self.escape_options.visible == True:
                    self.escape_options.hide_options()
                elif self.escape_options.visible == False:
                    self.escape_options.show_options()
            elif event.key() == Qt.Key_W:
                self.game_board.move_player('Up', player)
                self.game_board.move_enemy()
            elif event.key() == Qt.Key_S:
                self.game_board.move_player('Down', player)
                self.game_board.move_enemy()
            elif event.key() == Qt.Key_A:
                self.game_board.move_player('Left', player)
                self.game_board.move_enemy()
            elif event.key() == Qt.Key_D:
                self.game_board.move_player('Right', player)
                self.game_board.move_enemy()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    Core_Window = MenuWindow()
    sys.exit(app.exec_())

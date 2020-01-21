from PyQt5.Qt import QMdiSubWindow

import datetime as dt
import os
import psycopg2

import SB_Characters as SBC
import SB_Professions as SBP
import SB_Objects as SBO
import SB_WidgetsClass as SBWC


class Options:

    def __init__(self, window):

        self.options = QMdiSubWindow(window)
        self.options.setGeometry(600, 20, 400, 600)
        self.list_of_slots = []
        self.save_path = os.getcwd() + "/saved_games/"
        self.game_loaded = False
        self.visible = False
        self.options.hide()

        # Buttons #
        self.save_game = SBWC.ButtonObject('Save Game', self.options, 150, 150, 'save_game_but')
        self.save_game.activate_event(self.save_game_to_database)

        self.load_game = SBWC.ButtonObject('Load Game', self.options, 150, 200, 'load_game_but')
        self.load_game.activate_event(self.load_game_to_gamemap)

        # Load Game slots #
        ''' Use 5 labels to display saved games, each saved game is named after it's timestamp.
            Side PyQt5 slider allows to scroll down the list of saved games. As you move the
            slider, the values attached to labels change. So instead of using 100 labels for 100
            saved games, it's using only 5 labels for infinite amount of saved games.'''
        self.show_saved_game_01 = SBWC.LabelObject(self.options, "", 50, 150, "save_001")
        self.show_saved_game_02 = SBWC.LabelObject(self.options, "", 50, 200, "save_002")
        self.show_saved_game_03 = SBWC.LabelObject(self.options, "", 50, 250, "save_003")
        self.show_saved_game_04 = SBWC.LabelObject(self.options, "", 50, 300, "save_004")
        self.show_saved_game_05 = SBWC.LabelObject(self.options, "", 50, 350, "save_005")

        self.list_of_slots.extend([self.show_saved_game_01, self.show_saved_game_02,
                                   self.show_saved_game_03, self.show_saved_game_04,
                                   self.show_saved_game_05])
        # Slider
        self.saves_slider = SBWC.SlideObject(self.options, len(self.list_of_slots) - 1, self.slide_saves)

        ''' Quite inconvenient way for loading saved games. You need to move slider to see saved
            games, most recent, top to bottom. Then, out of 5 on display, you have to pick the one 
            that you want to load, by using the up and down button. Finally, to load the game, you 
            have to press the load button. This solution to save/load game was used only as a 
            showcase example.
            Other save/load game solutions are at the bottom of this file.
        '''
        self.pick_save = SBWC.ButtonObject('Load' + str(self.list_of_slots[0].object_data), self.options, 50, 425,
                                          'select_save_slot')
        self.pick_save.new_button.resize(250, 40)
        self.pick_save.activate_event(self.pick_this_game)

        self.pick_up = SBWC.ButtonObject('^', self.options, 300, 150, 'up_save_slots')
        self.pick_up.new_button.resize(25, 25)
        self.pick_up.activate_event(self.pick_save_up)

        self.pick_down = SBWC.ButtonObject('v', self.options, 300, 200, 'down_save_slots')
        self.pick_down.new_button.resize(25, 25)
        self.pick_down.activate_event(self.pick_save_down)

    def show_options(self):
        if not self.visible:
            self.options.show()
            self.visible = True

    def hide_options(self):
        self.options.hide()
        self.visible = False

    def pick_this_game(self):
      try:
        game_to_load = str(self.pick_save.name[6:len(self.pick_save.name) - 1])

        conn = psycopg2.connect(database=game_to_load, user="postgres", password="", host="127.0.0.1", port="5432")
        cur = conn.cursor()

        cur.execute("SELECT * from player_data")
        player_data = cur.fetchall()
        for data in player_data:
            for profession in SBP.list_of_professions:
                if profession.name == data[3]:
                    load_profession = profession
            print(data[4])
            New_Player = SBC.Player(data[1], data[2], load_profession, data[4][45:], data[5], data[6], data[7])
            SBC.list_of_players_on_the_map.append(New_Player)

        cur.execute("SELECT * FROM player_inventory")
        player_inventory = cur.fetchall()

        cur.execute("SELECT * FROM monsters_data")
        monster_data = cur.fetchall()
        for data in monster_data:
            print(data)
            for profession in SBP.list_of_professions:
                if profession.name == data[3]:
                    load_profession = profession
            New_Monster = SBC.Monster(data[1], data[2], load_profession, data[4][45:], data[5], data[6], data[7])
            SBC.list_of_monster_on_the_map.append(New_Monster)

        cur.execute("SELECT * FROM objects_data")
        objects_data = cur.fetchall()

        for data in objects_data:
            New_Wall = SBO.Wall(data[1], data[2], data[3], data[4], data[5], data[6][48:], data[7], data[8])
            SBO.list_of_walls_on_the_map.append(New_Wall)

        cur.close()
        conn.close()
        self.game_loaded = True
        self.options.visible = False
        self.hide_options()

      except Exception as e:
          print(e)
    def pick_save_up(self):
        if self.pick_save.scroll >= -4:
            self.pick_save.scroll -= 1
            name = "Load: " + str(self.list_of_slots[self.pick_save.scroll].object_data)
            self.pick_save.new_button.hide()
            self.pick_save.new_button.setText(name)
            self.pick_save.name = name
            self.pick_save.new_button.show()
            if self.pick_save.scroll == -5:
                self.pick_save.scroll = 0

    def pick_save_down(self):
        if self.pick_save.scroll <= len(self.list_of_slots) - 1:
            self.pick_save.scroll += 1
            name = "Load: " + str(self.list_of_slots[self.pick_save.scroll].object_data)
            self.pick_save.new_button.hide()
            self.pick_save.new_button.setText(name)
            self.pick_save.name = name
            self.pick_save.new_button.show()
            if self.pick_save.scroll == 4:
                self.pick_save.scroll -= 1

    def save_game_to_database(self):
        save_name = dt.datetime.now()
        data = str(save_name.strftime("saved_game_%m_%d_%y_%H_%M_%S"))
        with psycopg2.connect(user="postgres", password="", host="127.0.0.1", port="5432") as conn:
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            ''' Create a new database for each new save slot. It's not the most efficient solution,
                but for the purpose of this example project, it works. This whole section is mainly
                for showing SQL-based solution. Using SQL for single player, non-online game is 
                not optimal.
                It could be useful if the game would send some data to the web-server like:
                Who got how far, so you can compete.
                Characters ladderboard etc.
                Although it's still unnecessary to use SQL for game saving/loading.'''

            with conn.cursor() as cur:
                cur.execute("CREATE DATABASE %s;" % data)

        def create_tables():
          try:
            conn = psycopg2.connect(database=data, user="postgres", password="", host="127.0.0.1", port="5432")
            cur = conn.cursor()

            cur.execute('''CREATE TABLE player_data
                            (ID INT PRIMARY KEY NOT NULL,
                            PLAYER_NAME TEXT NOT NULL,
                            PLAYER_LEVEL INT NOT NULL,
                            PLAYER_PROF TEXT NOT NULL,
                            PLAYER_IMAGE TEXT NOT NULL,
                            PLAYER_IDTAG INT NOT NULL,
                            PLAYER_X INT NOT NULL,
                            PLAYER_Y INT NOT NULL);
                            ''')
            conn.commit()

            cur.execute('''CREATE TABLE player_inventory
                                        (ID INT PRIMARY KEY NOT NULL,
                                        ITEM_NAME TEXT NOT NULL);''')
            conn.commit()

            cur.execute('''CREATE TABLE monsters_data
                                        (ID INT PRIMARY KEY NOT NULL,
                                        MONSTER_NAME TEXT NOT NULL,
                                        MONSTER_LEVEL INT NOT NULL,
                                        MONSTER_PROF TEXT NOT NULL,
                                        MONSTER_IMAGE TEXT NOT NULL,
                                        MONSTER_IDTAG INT NOT NULL,
                                        MONSTER_X INT NOT NULL,
                                        MONSTER_Y INT NOT NULL);
                                        ''')
            conn.commit()

            cur.execute('''CREATE TABLE objects_data
                        (ID INT PRIMARY KEY NOT NULL,
                        OBJECT_NAME TEXT NOT NULL,
                        OBJECT_PATTERN INT NOT NULL,
                        OBJECT_TILES INT NOT NULL,
                        OBJECT_WALK BOOLEAN NOT NULL,
                        OBJECT_DESTRUCTIBLE BOOLEAN NOT NULL,
                        OBJECT_IMAGE TEXT NOT NULL,
                        OBJECT_X INT NOT NULL,
                        OBJECT_Y INT NOT NULL);
                        ''')
            conn.commit()

            cur.close()
            conn.close()
          except Exception as e:
              print(e)
        create_tables()

        ######TODO:#########################
        # Write some more save/load systems
        ######

        def insert_data():
          try:
            conn = psycopg2.connect(database=data, user='postgres', password='', host='127.0.0.1', port='5432')
            cur = conn.cursor()
            for player in SBC.list_of_players_on_the_map:
                query = '''INSERT INTO player_data(ID, PLAYER_NAME, PLAYER_LEVEL, PLAYER_PROF,
                    PLAYER_IMAGE, PLAYER_IDTAG, PLAYER_X, PLAYER_Y)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
                player_data = (1, str(player.name), int(player.level),
                               str(player.profession.name), str(player.game_image), int(player.id_tag), int(player.cordx), int(player.cordy))
                cur.execute(query, player_data)
                conn.commit()

                item_id = 0
                for item in player.inventory:
                    item_id += 1
                    query = 'INSERT INTO player_inventory(ID, ITEM_NAME) VALUES(%s, %s)'
                    item_data = (item_id, str(item.name))
                    cur.execute(query, item_data)
                    conn.commit()

            monster_id = 0
            objects_id = 0
            for item in SBC.list_of_monster_on_the_map:
                monster_id += 1
                query = '''INSERT INTO monsters_data(ID, MONSTER_NAME, MONSTER_LEVEL, 
                          MONSTER_PROF, MONSTER_IMAGE, MONSTER_IDTAG, MONSTER_X, MONSTER_Y)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
                monster_data = (
                monster_id, str(item.name), int(item.level), str(item.profession), str(item.game_image),
                int(item.id_tag), int(item.cordx), int(item.cordy))
                cur.execute(query, monster_data)
                conn.commit()

            for item in SBO.list_of_walls_on_the_map:
                objects_id += 1
                query = "INSERT INTO objects_data(ID, OBJECT_NAME, OBJECT_PATTERN, OBJECT_TILES," \
                        " OBJECT_WALK, OBJECT_DESTRUCTIBLE, OBJECT_IMAGE, OBJECT_X, OBJECT_Y)" \
                        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                object_data = (objects_id, str(item.name), int(item.pattern),
                               int(item.tiles), bool(item.walkable), bool(item.destructible), str(item.game_image),
                               int(item.cordx), int(item.cordy))
                cur.execute(query, object_data)
                conn.commit()
          except Exception as e:
              print(e)
        insert_data()
        cur.close()
        conn.close()

        with open(self.save_path + "/saved_games_list.txt", "a") as file:
            file.write(str(data) + "\n")

    def load_game_to_gamemap(self):

        self.save_game.new_button.hide()
        self.load_game.new_button.hide()
        self.saves_slider.new_slider.show()

        with open(self.save_path + "/saved_games_list.txt") as file:
            data = file.readlines()

            i = 0
            z = len(data) - 1
            self.saves_slider.slider_value(z)
            self.saves_slider.slider_set_max_value(z)
            while i <= len(self.list_of_slots) - 1:
                if z >= len(data) - 1:
                    self.list_of_slots[i].new_label.setText("Load: " + str(data[z]))
                    self.list_of_slots[i].attach_object(str(data[z]))
                i += 1
                z -= 1
            for item in self.list_of_slots:
                if item.object_data:
                    item.new_label.resize(250, 50)
                    item.new_label.show()
            self.pick_save.new_button.setText("Load: " + str(self.list_of_slots[0].object_data))
            self.pick_save.name = "Load: " + str(self.list_of_slots[0].object_data)
            self.pick_save.new_button.show()
            self.pick_down.new_button.show()
            self.pick_up.new_button.show()

    def slide_saves(self, value):
        with open(self.save_path + "/saved_games_list.txt") as file:
            data = file.readlines()
            i = 0
            z = value
            while i <= len(self.list_of_slots) - 1 and z >= 0:
                self.list_of_slots[i].new_label.setText("Load: " + str(data[z]))
                self.list_of_slots[i].attach_object(str(data[z]))
                i += 1
                z -= 1


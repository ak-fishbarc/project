# This is a draft version of this project.
'''
It still needs a lot of work, but finishing everything would take a lot of time.
Unfortunately I have only around 2 hours a day, on days when I can learn python.
For that reason, I'm sending this as a showcase project.
Main reason for using PyQt5 instead of PyGame or Pyglet is that PyQt5 offers more
problems and challenge.
I was trying to make this project problematic to stretch myself.
I choose game as a project as it seems to be more difficult than building a simple
program for browsing files or scraping data of the internet, etc.
'''

import sys
import socket
import threading
import select
import asyncio
import pickle
import re

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import SB_GameMapv002 as SBGM
import SB_Characters as SBC
import SB_WidgetsClass as SBWC
import SB_Inventory as SBI
import SB_ESCOptions as SBESC
import SB_Objects as SBOB
import SB_Professions as SBP
import SB_SpellList as SBSL


class MenuWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Spellbook v.0.0.2'
        self.height = 800
        self.width = 640

        self.game_is_on = False

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        self.main_menu = QMdiSubWindow(self)
        self.main_menu.hide()

        self.create_char = QMdiSubWindow(self)
        self.create_char.hide()

        self.options = SBESC.Options(self)

        self.game_display = QMdiSubWindow(self)
        self.game_display.hide()

        self.game_board = None
        self.list_of_maps = []
        self.player_list = []

        self.network_game = QMdiSubWindow(self)
        self.network_game.hide()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(400, 100, self.height, self.width)

        self.initMenu()

        self.show()

    def initMenu(self):
        self.main_menu.setWindowTitle('Main Menu')
        self.main_menu.setGeometry(0, 0, self.height, self.width)

        new_game = SBWC.ControlButtons('New Game', self.main_menu, 350, 150, 'new_game_but')
        new_game.activate_this(self.start_new_game)

        load_game = SBWC.ControlButtons('Load Game', self.main_menu, 350, 200, 'load_game_but')
        load_game.activate_this(self.load_game_options)

        multiplayer = SBWC.ControlButtons('Multiplayer', self.main_menu, 350, 250, 'multi_game_but')
        multiplayer.activate_this(self.multiplayer_game)

        self.main_menu.show()

    #def PlaceHolder(self):
    #   self.initGameMap(SBC.Player1, SBC.list_of_monsters, SBOB.list_of_walls)

    # This version of multiplayer game is not working correctly. It does not send and recieve
    # data correctly for all players.
    # Most of problems come from player1 using hosting server as the client.
    
    def multiplayer_game(self):
        self.game_msg = None
        self.map_msg = None
        self.host_msg = None
        self.player22 = None
        self.player2 = SBWC.Label('', self.network_game, 0, 0, 'A')
        network_char = SBC.Player1


        def start_host_game():
            host_game.hide_self()
            join_game.hide_self()

            def ntwrk_player_name():
                network_char.name = player_name.textBox.text()
                stats_text = 'Name: {} \n' \
                             'Class: {} \n' \
                             'Level: {} \n' \
                             'Strength: {} \n' \
                             'Dexterity: {} \n' \
                             'Endurance: {} \n' \
                             'Intelligence: {} \n' \
                             'Wisdom: {} \n' \
                             'Health: {} \n' \
                             'Armor: {}'.format(network_char.name, network_char.prof.name,
                                                network_char.level, network_char.stg,
                                                network_char.dex, network_char.end,
                                                network_char.ing, network_char.wis,
                                                network_char.hp, network_char.armor)
                display_stats.change_text(stats_text)

            stats_text = 'Name: {} \n' \
                             'Class: {} \n' \
                             'Level: {} \n' \
                             'Strength: {} \n' \
                             'Dexterity: {} \n' \
                             'Endurance: {} \n' \
                             'Intelligence: {} \n' \
                             'Wisdom: {} \n' \
                             'Health: {} \n' \
                             'Armor: {}'.format(network_char.name, network_char.prof.name,
                                                network_char.level, network_char.stg,
                                                network_char.dex, network_char.end,
                                                network_char.ing, network_char.wis,
                                                network_char.hp, network_char.armor)

            player_name = SBWC.TextInput('Player Name', self.network_game, 250, 100, 100, 25)
            player_name.textBox.show()
            player_name.textBox.returnPressed.connect(ntwrk_player_name)
            display_stats = SBWC.Label('Stats', self.network_game, 350, 100, 'Stats')
            display_stats.change_size(250, 300)
            display_stats.change_text(stats_text)
            display_stats.label.show()
            create_char = SBWC.ControlButtons('Create Character', self.network_game, 500, 300, 'Create Char')
            create_char.show_self()

            def send_player_data():
                self.game_msg = b'0001 ' + pickle.dumps(network_char)
                self.network_game.hide()
                player_name.textBox.hide()
                display_stats.label.hide()
                create_char.hide_self()
                chat_name.move_self(260, 500)
                chat_name.change_text('Chat:')
                chat_entry_box.textBox.move(300, 500)
                self.initNetworkGame(network_char)

            pre_pickled = pickle.dumps(network_char)
            def server_listen():

                print('Server up and running!')
                host_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                host_server.setblocking(0)
                host = socket.gethostname()
                port = 12345
                host_server.bind((host, port))
                host_server.listen(4)

                is_readable = [host_server]
                is_writable = []
                is_error = []
                message_list = {}
                print(host_server)
                while True:

                    ready_read, ready_write, err_soc = select.select(is_readable, is_writable, is_error, 1.0)
                    for soc in ready_read:
                        if soc is host_server:
                            con, addr = soc.accept()
                            con.sendall(b'0001 ' + pre_pickled)
                            con.setblocking(0)
                            print(self.game_msg)
                            is_readable.append(con)
                        else:
                            if soc not in is_writable:
                                is_writable.append(soc)
                            data = soc.recv(1024)
                            if data:
                                print(data)
                                lookfor = re.search(b'^0001|^0002', data)
                                if lookfor:
                                    if data[:5] == b'0002 ':
                                        clean_data = data[5:]
                                        if clean_data == b'Up':
                                            for player in self.player_list:
                                                if player != SBC.Player1:
                                                    self.game_board.board[player.posx][player.posy] = 0
                                                    self.game_board.board[player.posx - 1][player.posy] = player
                                                    self.player2.move_self(self.player2.x, self.player2.y - 50)
                                                    self.player2.y -= 50
                                                    player.posx -= 1
                                        if clean_data == b'Down':
                                            for player in self.player_list:
                                                if player != SBC.Player1:
                                                    self.game_board.board[player.posx][player.posy] = 0
                                                    self.game_board.board[player.posx + 1][player.posy] = player
                                                    self.player2.move_self(self.player2.x, self.player2.y + 50)
                                                    self.player2.y += 50
                                                    player.posx += 1
                                        if clean_data == b'Right':
                                            for player in self.player_list:
                                                if player != SBC.Player1:
                                                    self.game_board.board[player.posx][player.posy] = 0
                                                    self.game_board.board[player.posx][player.posy + 1] = player
                                                    self.player2.move_self(self.player2.x + 50, self.player2.y)
                                                    self.player2.x += 50
                                                    player.posy += 1
                                        if clean_data == b'Left':
                                            for player in self.player_list:
                                                if player != SBC.Player1:
                                                    self.game_board.board[player.posx][player.posy] = 0
                                                    self.game_board.board[player.posx][player.posy - 1] = player
                                                    self.player2.move_self(self.player2.x - 50, self.player2.y)
                                                    self.player2.x -= 50
                                                    player.posy -= 1
                                        print(self.game_board.board)
                                    if data[:5] == b'0001 ':
                                        clean_data = data[5:]
                                        game_data = pickle.loads(clean_data)
                                        print(game_data)
                                        if game_data:
                                            self.player22 = game_data
                                            self.player_list.append(self.player22)
                                            self.game_board.board[self.player22.posx][self.player22.posy] = self.player22
                                            self.player2.add_object(self.game_board.board[self.player22.posx][self.player22.posy])
                                            num_of_x = 0
                                            num_of_y = 0
                                            xpos = 175
                                            ypos = 50
                                            for x in self.game_board.board:
                                                for y in x:
                                                    if self.game_board.board[num_of_x][num_of_y] == self.player22:
                                                        self.player2.move_self(xpos, ypos)
                                                        self.player2.x = xpos
                                                        self.player2.y = ypos
                                                    xpos += 50
                                                    num_of_y += 1
                                                ypos += 50
                                                xpos = 175
                                                num_of_x += 1
                                                num_of_y = 0
                                            self.player2.change_image(self.player22.prof.game_image)
                                            self.game_board.list_of_objects.append(self.player2)
                                            self.player2.show_self()
                                            print('Tutuutuutu')


                                message_list[soc] = data

                    if message_list:
                        print(message_list)
                    for soc in is_writable:
                        if message_list:
                            for message in message_list:
                                soc.send(message_list[message])
                        if self.host_msg:
                                soc.send(self.host_msg.encode())
                                print(self.host_msg)
                        if self.game_msg:
                                soc.send(self.game_msg)

                    self.host_msg = None
                    self.game_msg = None
                    message_list.clear()

            create_char.activate_this(send_player_data)
            chat_display.show_self()

            t = threading.Thread(target=server_listen)
            t.start()

        def msg_ready():
            self.host_msg = chat_entry_box.textBox.text()
            chat_entry_box.textBox.setText('')
            print(self.host_msg)

        chat_entry_box = SBWC.TextInput('Chatbox', self.network_game, 420, 350, 250, 25)
        chat_entry_box.textBox.returnPressed.connect(msg_ready)
        chat_entry_box.textBox.show()

        def start_client_game():
            host_game.hide_self()
            join_game.hide_self()

            def ntwrk_player_name():
                network_char.name = player_name.textBox.text()
                stats_text = 'Name: {} \n' \
                             'Class: {} \n' \
                             'Level: {} \n' \
                             'Strength: {} \n' \
                             'Dexterity: {} \n' \
                             'Endurance: {} \n' \
                             'Intelligence: {} \n' \
                             'Wisdom: {} \n' \
                             'Health: {} \n' \
                             'Armor: {}'.format(network_char.name, network_char.prof.name,
                                                network_char.level, network_char.stg,
                                                network_char.dex, network_char.end,
                                                network_char.ing, network_char.wis,
                                                network_char.hp, network_char.armor)
                display_stats.change_text(stats_text)

            stats_text = 'Name: {} \n' \
                         'Class: {} \n' \
                         'Level: {} \n' \
                         'Strength: {} \n' \
                         'Dexterity: {} \n' \
                         'Endurance: {} \n' \
                         'Intelligence: {} \n' \
                         'Wisdom: {} \n' \
                         'Health: {} \n' \
                         'Armor: {}'.format(network_char.name, network_char.prof.name,
                                            network_char.level, network_char.stg,
                                            network_char.dex, network_char.end,
                                            network_char.ing, network_char.wis,
                                            network_char.hp, network_char.armor)

            player_name = SBWC.TextInput('Player Name', self.network_game, 250, 100, 100, 25)
            player_name.textBox.show()
            player_name.textBox.returnPressed.connect(ntwrk_player_name)
            display_stats = SBWC.Label('Stats', self.network_game, 350, 100, 'Stats')
            display_stats.change_size(250, 300)
            display_stats.change_text(stats_text)
            display_stats.label.show()
            create_char = SBWC.ControlButtons('Create Character', self.network_game, 500, 300, 'Create Char')
            create_char.show_self()

            def send_player_data():
                self.game_msg = b'0001 ' + pickle.dumps(network_char)
                self.network_game.hide()
                player_name.textBox.hide()
                display_stats.label.hide()
                create_char.hide_self()
                chat_name.move_self(260, 500)
                chat_name.change_text('Chat:')
                chat_entry_box.textBox.move(300, 500)
                self.initNetworkGame(network_char)

            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = socket.gethostname()
            port = 12345

            def client_connect():

                async def write_msg():

                        if self.host_msg:
                            c.send(self.host_msg.encode())
                            self.host_msg = None
                        if self.game_msg:
                            c.send(self.game_msg)
                            self.game_msg = None
                        await asyncio.sleep(0.5)

                async def listen_to():
                           try:
                                data = c.recv(1024)
                                lookfor = re.search(b'^0001|^0002|^0003', data)
                                if lookfor:
                                    print(data[:5])
                                    if data[:5] == b'0002 ':
                                        clean_data = data[5:]
                                        self.recv_data = clean_data
                                        print(clean_data)
                                    if data[:5] == b'0001 ':
                                        clean_data = data[5:]
                                        game_data = pickle.loads(clean_data)
                                        print(game_data)
                                    if data[:5] == b'0003 ':
                                        clean_data = data[5:]
                                        map_data = pickle.loads(clean_data)
                                        print(map_data)
                                    print(self.game_board.board)
                                else:
                                    print(data)
                           except Exception:
                               await asyncio.sleep(1.0)

                try:

                    c.connect((host, port))
                    c.sendall(b'Connected to the server')


                    while True:
                        c.setblocking(0)
                        asyncio.run(write_msg())
                        asyncio.run(listen_to())


                except Exception as e:
                    print(e)

            create_char.activate_this(send_player_data)

            t = threading.Thread(target=client_connect)
            t.start()

        self.main_menu.hide()
        self.network_game.setWindowTitle('Network Game')
        self.network_game.setGeometry(0, 0, self.height, self.width)

        host_game = SBWC.ControlButtons('Host Game', self.network_game, 350, 100, 'host_game_but')
        host_game.activate_this(start_host_game)
        join_game = SBWC.ControlButtons('Join Game', self.network_game, 350, 150, 'join_game_but')
        join_game.activate_this(start_client_game)

        chat_name = SBWC.Label('', self.network_game, 350, 350, 'network')
        chat_name.change_text('Lobby Chat: ')
        chat_name.change_size(75, 25)
        chat_display = SBWC.Label('', self.network_game, 350, 400, 'network_chat')
        chat_display.change_size(300, 400)
        chat_display.hide_tile()

        self.network_game.show()

    def initNetworkGame(self, host_player):
        self.player_list = []
        self.player_list.append(host_player)

        try:

            self.game_is_on = True
            self.game_board = SBGM.GameMap()
            self.list_of_maps.append(self.game_board)
            for player in self.player_list:
                player.show_inventory = SBI.Inventory(self, player)
                player.show_inventory.hide_inv()
            self.game_board.board[host_player.posx][host_player.posy] = host_player
            self.game_board.create_map(self.network_game)

            self.network_game.show()
        except Exception as e:
          print(e)


    def load_game_options(self):
        self.main_menu.hide()
        self.options.load_game_to_gm()
        self.options.show_options()

    def start_new_game(self):
        self.main_menu.hide()
        self.initCharCreate()

    def initCharCreate(self):

        stats_text = 'Name: {} \n' \
                     'Class: {} \n' \
                     'Level: {} \n' \
                     'Strength: {} \n' \
                     'Dexterity: {} \n' \
                     'Endurance: {} \n' \
                     'Intelligence: {} \n' \
                     'Wisdom: {} \n' \
                     'Health: {} \n' \
                     'Armor: {}'.format(SBC.Player1.name, SBC.Player1.prof.name,
                                        SBC.Player1.level, SBC.Player1.stg,
                                        SBC.Player1.dex, SBC.Player1.end,
                                        SBC.Player1.ing, SBC.Player1.wis,
                                        SBC.Player1.hp, SBC.Player1.armor)

        def change_name():
            SBC.Player1.name = str(enter_name.textBox.text())
            stats_text = 'Name: {} \n' \
                         'Class: {} \n' \
                         'Level: {} \n' \
                         'Strength: {} \n' \
                         'Dexterity: {} \n' \
                         'Endurance: {} \n' \
                         'Intelligence: {} \n' \
                         'Wisdom: {} \n' \
                         'Health: {} \n' \
                         'Armor: {}'.format(SBC.Player1.name, SBC.Player1.prof.name,
                                            SBC.Player1.level, SBC.Player1.stg,
                                            SBC.Player1.dex, SBC.Player1.end,
                                            SBC.Player1.ing, SBC.Player1.wis,
                                            SBC.Player1.hp, SBC.Player1.armor)
            show_stats.change_text(stats_text)

        list_of_barb = []
        list_of_wizard = []

        def display_skills(window):
         try:
            def create_labels(prof_name, list_name):

              x = 600
              y = 200
              for item in SBSL.list_of_skilltrees:
                 if item.name == prof_name:
                    print(item.name)
                    print(prof_name)
                    for skill in item.tier1:
                        skill_label = SBWC.Label(str(skill.image), window, x, y, skill.name)
                        skill_name_label = SBWC.Label('', window, x, y - 25, skill.name)
                        skill_name_label.change_text(str(skill.name))
                        skill_name_label.change_size(90, 25)
                        list_name.append(skill_label)
                        list_name.append(skill_name_label)
                        x += 50
                    x = 500
                    y = 280
                    for skill in item.tier2:
                        skill_label = SBWC.Label(str(skill.image), window, x, y, skill.name)
                        skill_name_label = SBWC.Label('', window, x, y - 25, skill.name)
                        skill_name_label.change_text(str(skill.name))
                        skill_name_label.change_size(90, 25)
                        list_name.append(skill_label)
                        list_name.append(skill_name_label)
                        x += 50
                    x = 450
                    y = 330
                    for skill in item.tier3:
                        skill_label = SBWC.Label(str(skill.image), window, x, y, skill.name)
                        skill_name_label = SBWC.Label('', window, x, y - 25, skill.name)
                        skill_name_label.change_text(str(skill.name))
                        skill_name_label.change_size(90, 25)
                        list_name.append(skill_label)
                        list_name.append(skill_name_label)
                        x += 50
                    x = 400
                    y = 380
                    for skill in item.tier4:
                        skill_label = SBWC.Label(str(skill.image), window, x, y, skill.name)
                        skill_name_label = SBWC.Label('', window, x, y - 25, skill.name)
                        skill_name_label.change_text(str(skill.name))
                        skill_name_label.change_size(90, 25)
                        list_name.append(skill_label)
                        list_name.append(skill_name_label)
                        x += 50
                    x = 350
                    y = 430
                    for skill in item.tier5:
                        skill_label = SBWC.Label(str(skill.image), window, x, y, skill.name)
                        skill_name_label = SBWC.Label('', window, x - 15, y - 25, skill.name)
                        skill_name_label.change_text(str(skill.name))
                        skill_name_label.change_size(90, 25)
                        list_name.append(skill_label)
                        list_name.append(skill_name_label)
                        x += 50

            for item in SBSL.list_of_skilltrees:
                if item.name == SBC.Player1.prof.name:
                    if item.name == 'Barbarian' and len(list_of_barb) == 0:
                        if len(list_of_wizard) > 0:
                            for label in list_of_wizard:
                                label.hide_tile()
                        create_labels('Barbarian', list_of_barb)
                    elif item.name == 'Wizard' and len(list_of_wizard) == 0:
                        if len(list_of_barb) > 0:
                            for label in list_of_barb:
                                label.hide_tile()
                        create_labels('Wizard', list_of_wizard)
                        for label in list_of_wizard:
                            label.show_self()
                    elif item.name == 'Barbarian' and len(list_of_barb) > 0:
                        if len(list_of_wizard) > 0:
                            for label in list_of_wizard:
                                label.hide_tile()
                        for label in list_of_barb:
                            label.show_self()
                    elif item.name == 'Wizard' and len(list_of_wizard) > 0:
                        if len(list_of_barb) > 0:
                            for label in list_of_barb:
                                label.hide_tile()
                        for label in list_of_wizard:
                            label.show_self()
         except Exception as e:
             print(e)

        def change_class():
            new_prof = str(pick_class.box_com.currentText())
            for prof in SBP.list_of_professions:
                if new_prof == prof.name:
                    SBC.Player1.prof = prof
                    SBC.Player1.set_stats()
            stats_text = 'Name: {} \n' \
                         'Class: {} \n' \
                         'Level: {} \n' \
                         'Strength: {} \n' \
                         'Dexterity: {} \n' \
                         'Endurance: {} \n' \
                         'Intelligence: {} \n' \
                         'Wisdom: {} \n' \
                         'Health: {} \n' \
                         'Armor: {}'.format(SBC.Player1.name, SBC.Player1.prof.name,
                                            SBC.Player1.level, SBC.Player1.stg,
                                            SBC.Player1.dex, SBC.Player1.end,
                                            SBC.Player1.ing, SBC.Player1.wis,
                                            SBC.Player1.hp, SBC.Player1.armor)
            show_stats.change_text(stats_text)
            show_image.change_image(SBC.Player1.prof.menu_image)
            display_skills(self.create_char)

        self.create_char.setWindowTitle('Create Character')
        self.create_char.setGeometry(0, 0, self.height, self.width)

        display_skills(self.create_char)

        enter_name = SBWC.TextInput('Player Name', self.create_char, 50, 100, 100, 25)
        enter_name.textBox.returnPressed.connect(change_name)

        pick_class = SBWC.Combox(self.create_char, 50, 150, *SBP.list_of_professions)
        pick_class.box_com.activated.connect(change_class)

        show_image = SBWC.Label(SBC.Player1.prof.menu_image, self.create_char, 320, 200, '')
        show_image.change_size(150, 150)

        show_stats = SBWC.Label('', self.create_char, 200, 200, '')
        show_stats.change_size(200, 150)
        show_stats.change_text(stats_text)

        start_game = SBWC.ControlButtons('Start Game', self.create_char, 600, 400, 'start_game_but')
        start_game.activate_this(self.initGameDisplay)

        self.create_char.show()

    def initGameDisplay(self):
        self.create_char.hide()
        self.initGameMap(SBC.Player1, SBC.list_of_monsters, SBOB.list_of_walls)
        print(SBC.Player1.name)
        print(SBC.Player1.prof.name)

    def initGameMap(self, *objects):
        player1 = None
        monsters = None
        walls = None
        length = len(objects) - 1
        if length >= 0:
            player1 = objects[0]
            self.player_list = []
            self.player_list.append(player1)
        if length >= 1:
            monsters = objects[1]
        if length >= 2:
            walls = objects[2]
        print(player1)
        print(self.player_list)
        for player in self.player_list:
            player.show_inventory = SBI.Inventory(self, player)
            player.show_inventory.hide_inv()

        self.game_display.setWindowTitle('Game Display')
        self.game_display.setGeometry(0, 0, self.height, self.width)
        self.game_display.setWindowFlags(self.game_display.windowFlags() | Qt.FramelessWindowHint)

        self.game_is_on = True

        self.game_board = SBGM.GameMap()
        self.list_of_maps.append(self.game_board)

        print(self.list_of_maps)

        self.game_board.board[SBC.Player1.posx][SBC.Player1.posy] = SBC.Player1
        if monsters:
            for mon in monsters:
                self.game_board.board[mon.posx][mon.posy] = mon
        if walls:
            for wall in walls:
                self.game_board.board[wall.posx][wall.posy] = wall

        self.game_board.create_map(self.game_display)

        self.game_display.show()

    def clearGameMap(self):
        for item in self.game_board.list_of_objects:
            item.hide_tile()

    def keyPressEvent(self, event):
        if self.options.game_loaded == True:
            self.options.game_loaded = False
            self.initGameMap(SBC.Player1, SBC.list_of_monsters, SBOB.list_of_walls)
        if self.game_is_on:
            if event.key() == Qt.Key_Escape:
                if SBC.Player1.show_inventory.visible:
                    SBC.Player1.show_inventory.hide_inv()
                if self.options.visible == True:
                    self.options.hide_options()
                    self.game_is_on = True
                elif self.options.visible == False:
                    self.options.show_options()
                    self.game_is_on = False
            elif event.key() == Qt.Key_I:
                self.game_is_on = False
                if not SBC.Player1.show_inventory.visible:
                    SBC.Player1.show_inventory.open_inv()
                    SBC.Player1.show_inventory.visible = True
                elif SBC.Player1.show_inventory.visible:
                    SBC.Player1.show_inventory.hide_inv()
                    SBC.Player1.show_inventory.visible = False
            elif event.key() == Qt.Key_L:
                self.game_board.move_player('CastSpell')
            elif event.key() == Qt.Key_W:
                self.game_msg = b'0002 Up'
                self.game_board.move_player('Up')
                self.game_board.move_monster()
            elif event.key() == Qt.Key_S:
                self.game_msg = b'0002 Down'
                self.game_board.move_player('Down')
                self.game_board.move_monster()
            elif event.key() == Qt.Key_A:
                self.game_msg = b'0002 Left'
                self.game_board.move_player('Left')
                self.game_board.move_monster()
            elif event.key() == Qt.Key_D:
                self.game_msg = b'0002 Right'
                self.game_board.move_player('Right')
                self.game_board.move_monster()
        else:
            if event.key() == Qt.Key_Escape:
                if SBC.Player1.show_inventory.visible:
                    SBC.Player1.show_inventory.hide_inv()
                if self.options.visible == True:
                    self.options.hide_options()
                    self.game_is_on = True
                elif self.options.visible == False:
                    self.options.show_options()
                    self.game_is_on = False
            elif event.key() == Qt.Key_I:
                self.game_is_on = True
                if SBC.Player1.show_inventory.visible:
                    SBC.Player1.show_inventory.hide_inv()
                    SBC.Player1.show_inventory.visible = False
        print(self.game_board.board)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main_Window = MenuWindow()
    sys.exit(app.exec_())


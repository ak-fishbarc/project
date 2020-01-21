from PyQt5.Qt import QMdiSubWindow

import collections

import SB_WidgetsClass as SBWC


class Inventory:
    def __init__(self, window, player):
        self.inventory = QMdiSubWindow(window)
        self.inventory.setWindowTitle('Inventory')
        self.inventory.setGeometry(200, 100, 400, 400)
        #self.inventory.setWindowFlags(self.inventory.windowFlags() | Qt.FramelessWindowHint)
        self.visible = False
        self.player = player
        self.contains = []
        self.count_items = collections.Counter()
        self.show_items = []
        self.show_descriptions = []

    def open_inventory(self):
        posx = 50
        posy = 50
        for item in self.player.inventory:
            if item not in self.contains:
                self.contains.append(item)
                show_this_item = SBWC.LabelObject(self.inventory, item.inventory_image_image, posx, posy, item.name)
                self.show_items.append(show_this_item)
                item_description = SBWC.LabelObject(self.inventory, "", posx + 50, posy, item.name)
                self.show_descriptions.append(item_description)
                item_description.new_label.setText(item.description)
                item_description.new_label.resize(250, 25)
            else:
                print('Kwik')
                #######################UNDER CONSTRUCTION#########################################
            posy += 50
        self.inventory.show()

    def hide_inventory(self):
        self.inventory.hide()

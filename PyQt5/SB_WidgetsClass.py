from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QComboBox, QSlider
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore


class LabelObject:

    def __init__(self, window_name, pix_image, cordx, cordy, id):
        self.window = window_name
        self.pix_image = pix_image
        self.cordx = cordx
        self.cordy = cordy
        self.id = id

        self.object_data = ""

        self.new_label = QLabel(self.window)
        self.label_image = QPixmap(pix_image)
        self.new_label.setPixmap(self.label_image)
        self.new_label.move(cordx, cordy)
        self.new_label.resize(48, 48)

    def attach_object(self, object_data):
        self.object_data = object_data

    def change_image(self, image):
        self.label_image = QPixmap(image)
        self.new_label.setPixmap(self.label_image)


class ButtonObject:

    def __init__(self, name, window, cordx, cordy, id):
        self.name = name
        self.window = window
        self.cordx = cordx
        self.cordy = cordy
        self.id = id

        self.new_button = QPushButton(name, window)
        self.new_button.move(cordx, cordy)

        self.scroll = 0

    def activate_event(self, func):
        self.new_button.clicked.connect(func)


class TextInput:

    def __init__(self, window, cordx, cordy, height, width):
        self.text_box = QLineEdit(window)
        self.text_box.move(cordx, cordy)
        self.text_box.resize(height, width)


class ComboxObject:

    def __init__(self, window, cordx, cordy, *objects):
        self.new_box = QComboBox(window)
        self.new_box.move(cordx, cordy)
        for item in objects:
            self.new_box.addItem(str(item.name))


class SlideObject:

    def __init__(self, window, set_min_value, event_to_connect):
        self.new_slider = QSlider(window)
        self.new_slider.setGeometry(QtCore.QRect(275, 150, 16, 250))
        self.new_slider.setOrientation(QtCore.Qt.Vertical)
        self.new_slider.setMinimum(set_min_value)
        self.new_slider.valueChanged.connect(event_to_connect)

    def slider_value(self, set_value):
        self.new_slider.setValue(set_value)

    def slider_set_max_value(self, set_max_value):
        self.new_slider.setMaximum(set_max_value)

import sys
import os

from PyQt5.QtWidgets import QLabel, QMdiArea, QMainWindow, QMdiSubWindow, QApplication, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

image_dir = os.getcwd() + '/image/skills/'


class Skill:
    def __init__(self, name, image):
        self.name = name
        self.image = image_dir + image


rage = Skill('Rage', 'rage.png')
shatter = Skill('Shatter', 'shatter.png')
destroy = Skill('Destroy', 'rage.png')
kill = Skill('Kill', 'shatter.png')


class NewLabel:
    def __init__(self, window, name, image, x, y):
        self.new_label = QLabel(window)
        # Use name as an id
        self.name = name
        self.visible = True
        self.label_icon = QPixmap(image)

        self.new_label.setPixmap(self.label_icon)
        self.new_label.move(x, y)
        self.new_label.resize(48, 48)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Show - Skill Tree'
        self.height = 400
        self.width = 400

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        self.skill_labels = []

        self.skill_window = QMdiSubWindow(self)
        self.skill_window.hide()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(400, 400, self.height, self.width)

        self.create_skill_labels(self.skill_window, rage, shatter, destroy, kill)

        switch_on_off = QPushButton('Show/Hide', self.skill_window)
        switch_on_off.move(150, 100)
        switch_on_off.clicked.connect(self.show_hide)

        self.skill_window.setGeometry(0, 0, self.height, self.width)
        self.skill_window.setWindowFlags(self.skill_window.windowFlags() | Qt.FramelessWindowHint)
        self.skill_window.show()
        self.show()

    def show_hide(self):
        for label in self.skill_labels:
            # Labels could have their own methods to hide/show for convenience
            if label.visible:
                label.new_label.hide()
                label.visible = False
            else:
                label.new_label.show()
                label.visible = True

    def create_skill_labels(*args):
        window = args[0]
        skill_list = [x for x in args[2:]]
        label_x = 100
        label_y = 100
        for skill in skill_list:
            skill_label = NewLabel(window, skill.name, skill.image, label_x, label_y)
            label_y += 50
            window.skill_labels.append(skill_label)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main_Window = MainWindow()
    sys.exit(app.exec())

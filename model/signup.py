import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QToolButton, QPushButton)
from PyQt5.QtCore import Qt


class Signup(QWidget):
    def __init__(self):
        super().__init__()


        self.initUI()

    def initUI(self):
        self.setFixedSize(500, 700)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Signup()
    sys.exit(app.exec_())
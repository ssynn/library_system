import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout)
# from model import login
import login


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.bodyLayout = QGridLayout()
        self.setLogin()

        self.setGeometry(200, 200, 1280, 720)
        self.setFixedSize(1280, 720)
        self.setMyStyle()
        self.show()
        self.login.show()

    def setLogin(self):
        self.login = login.Login()
        self.login.loginButton.clicked.connect(self.loginFunction)
        self.login.signup.clicked.connect(self.signupFunction)
        # self.bodyLayout.addWidget(self.login)
        # self.setLayout(self.bodyLayout)

    def loginFunction(self):
        self.login.close()
        # self.temp = QGridLayout()
        # self.setLayout(self.temp)

    def signupFunction(self):
        self.login.close()

    def setMyStyle(self):
        self.setStyleSheet('''
        QWidget{
            background-color: white;
        }
        ''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

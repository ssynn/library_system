import sys
import hashlib
from PyQt5.QtWidgets import (QApplication, QWidget)
# from model import login
# from model import signup
# from model import database
import login
import signup
import database


# 密码
def encrypt(val):
    h = hashlib.sha256()
    password = val
    h.update(bytes(password, encoding='UTF-8'))
    result = h.hexdigest()
    return result


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setLogin()

        self.setGeometry(200, 200, 1280, 720)
        self.setFixedSize(1280, 720)
        self.setMyStyle()
        self.show()
        # self.login.show()

    # 创建登录菜单
    def setLogin(self):
        self.login = login.Login()
        self.login.setParent(self)
        self.login.move(390, 120)
        self.login.loginButton.clicked.connect(self.loginFunction)
        self.login.signup.clicked.connect(self.signupViewFunction)

    # 创建注册菜单
    def setSignup(self):
        self.signup = signup.Signup()
        self.signup.setParent(self)
        self.signup.setVisible(True)
        self.signup.move(425, 110)
        self.signup.back.clicked.connect(self.backToLogin)
        self.signup.submit.clicked.connect(self.signupFunction)

    # 登录按钮按下
    def loginFunction(self):
        user_mes = {
            'ID': self.login.accountInput.text(),
            'PASSWORD': encrypt(self.login.passwordInput.text())
        }
        self.user = database.signin(user_mes)
        if self.user is not None:
            self.login.setVisible(False)
            print(self.user)
            self.display()
        else:
            print('登录失败!')

    # 显示注册界面
    def signupViewFunction(self):
        self.login.setVisible(False)
        self.setSignup()

    # 注册按钮按下
    def signupFunction(self):
        for i in range(2, 9):
            item = self.signup.bodyLayout.itemAt(i).widget()
            if item.text() == item.initText:
                item.setText('')
        self.user_mes = {
            'SID': self.signup.accountInput.text(),
            'PASSWORD': encrypt(self.signup.passwordInput.text()),
            'SNAME': self.signup.nameInput.text(),
            'DEPARTMENT': self.signup.deptInput.text(),
            'MAJOR': self.signup.majorInput.text(),
            'MAX': int(self.signup.maxNumInput.text()),
            'PUNISHED': 0
        }
        self.user_mes['class'] = 'stu'
        self.user_mes.pop('PASSWORD')
        ans = database.signup(self.user_mes)
        if ans:
            self.signup.setVisible(False)
            print('成功')
            self.display()
        else:
            print('注册失败')

    def backToLogin(self):
        self.signup.setVisible(False)
        self.login.setVisible(True)

    def display(self):
        print(11)
        self.titleBar = QWidget()
        self.titleBar.setFixedSize(100, 50)
        self.titleBar.setParent(self)
        self.titleBar.setVisible(True)
        self.titleBar.move(10, 10)
        self.titleBar.setStyleSheet('''
        QWidget{
            background-color: rbga(44, 44, 44, 1);
            border: 1px;
        }
        ''')
        # self.bodyLayout = QGridLayout()
        # self.bodyLayout.addWidget(self.titleBar, 0, 0, 1, 7)
        # self.setLayout(self.bodyLayout)

    def setMyStyle(self):
        pass
        # self.setStyleSheet('''
        # QWidget{
        #     background-color: white;
        # }
        # ''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

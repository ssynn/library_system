import sys
from PyQt5.QtWidgets import (QApplication, QWidget)
# from model import login
# from model import signup
# from model import database
# form model import student
import login
import signup
import database
import student


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setLogin()

        self.setGeometry(200, 200, 1280, 720)
        self.setFixedSize(1280, 720)
        self.setMyStyle()
        self.show()

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
            'PASSWORD': database.encrypt(self.login.passwordInput.text())
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
        self.user = {
            'SID': self.signup.accountInput.text(),
            'PASSWORD': database.encrypt(self.signup.passwordInput.text()),
            'SNAME': self.signup.nameInput.text(),
            'DEPARTMENT': self.signup.deptInput.text(),
            'MAJOR': self.signup.majorInput.text(),
            'MAX': int(self.signup.maxNumInput.text()),
            'PUNISHED': 0
        }
        ans = database.signup(self.user)
        self.user['class'] = 'stu'
        self.user.pop('PASSWORD')
        if ans:
            self.signup.setVisible(False)
            print('成功')
            self.display()
        else:
            print('注册失败')

    def backToLogin(self):
        self.signup.setVisible(False)
        self.login.setVisible(True)

    def logout(self):
        self.body.close()
        self.login.setVisible(True)

    def display(self):
        # 显示学生信息
        if self.user['class'] == 'stu':
            self.body = student.StudentPage(self.user)
            self.body.setParent(self)
            self.body.setVisible(True)
            self.body.account.setText(self.user['SNAME'])
            self.body.out.clicked.connect(self.logout)

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

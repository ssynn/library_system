import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox)
from model import login
from model import signup
from model import database
from model import student
from model import administrator
# import login
# import signup
# import database
# import student
# import administrator


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setLogin()

        self.setGeometry(200, 200, 1280, 720)
        self.setFixedSize(1280, 720)
        self.setMyStyle()

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
            self.display()
        else:
            print('登录失败!')

    # 显示注册界面
    def signupViewFunction(self):
        self.login.setVisible(False)
        self.setSignup()

    # 注册按钮按下
    def signupFunction(self):
        '''
        获取信息后先检查
        把借书数量转为int
        加密密码
        '''
        self.user = self.signup.getInfo()
        res = database.check_user_info(self.user)
        if res['res'] == 'fail':
            self.errorBox(res['reason'])
            return
        self.user['MAX'] = int(self.user['MAX'])
        self.user['PASSWORD'] = database.encrypt(self.user['PASSWORD'])

        ans = database.signup(self.user)
        self.user['class'] = 'stu'
        self.user.pop('PASSWORD')
        if ans:
            self.signup.setVisible(False)
            print('成功')
            self.display()
        else:
            self.errorBox('注册失败')

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
            self.body.out.clicked.connect(self.logout)
        else:
            self.body = administrator.AdministratorPage(self.user)
            self.body.setParent(self)
            self.body.setVisible(True)
            self.body.out.clicked.connect(self.logout)

    def errorBox(self, mes: str):
        msgBox = QMessageBox(
            QMessageBox.Warning,
            "警告!",
            mes,
            QMessageBox.NoButton,
            self
        )
        msgBox.addButton("确认", QMessageBox.AcceptRole)
        msgBox.exec_()

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

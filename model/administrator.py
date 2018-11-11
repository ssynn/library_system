import sys
import time
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QGroupBox,
                             QToolButton, QSplitter, QVBoxLayout, QHBoxLayout,
                             QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView,
                             QLineEdit, QFileDialog)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize
# from model import database
# from model import book_information
import database
import book_information


class AdministratorPage(QWidget):
    def __init__(self, stu_mes):
        super().__init__()
        self.focus = 0
        self.stu_mes = stu_mes
        self.initUI()

    def initUI(self):
        # 标题栏
        self.titleBar = QWidget()
        self.titleBar.setFixedSize(1250, 50)
        self.setTitleBar()

        # 分割
        self.body = QSplitter()
        self.setLeftMunu()
        self.content = None
        self.setContent()

        self.bodyLayout = QGridLayout()
        self.bodyLayout.addWidget(self.titleBar, 0, 0, 1, 7)
        self.bodyLayout.addWidget(self.body, 1, 0, 7, 7)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.bodyLayout)
        self.setFixedSize(1280, 720)
        self.setMyStyle()

    # 设置标题栏
    def setTitleBar(self):
        self.title = QLabel()
        self.title.setText('欢迎使用图书馆管理系统')
        self.title.setFixedHeight(30)

        self.account = QToolButton()
        self.account.setIcon(QIcon('icon/person.png'))
        self.account.setText('ADMIN')
        self.account.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.account.setFixedHeight(20)
        self.account.setEnabled(False)

        self.out = QToolButton()
        self.out.setText('退出')
        self.out.setFixedHeight(30)

        titleLayout = QHBoxLayout()
        titleLayout.addSpacing(100)
        titleLayout.addWidget(self.title)
        titleLayout.addWidget(self.account)
        titleLayout.addWidget(self.out)
        self.titleBar.setLayout(titleLayout)

    # 左侧菜单栏
    def setLeftMunu(self):
        # 书籍管理
        self.bookManage = QToolButton()
        self.bookManage.setText('图书管理')
        self.bookManage.setFixedSize(160, 50)
        self.bookManage.setIcon(QIcon('icon/book.png'))
        self.bookManage.setIconSize(QSize(30, 30))
        self.bookManage.clicked.connect(
            lambda: self.switch(0, self.bookManage))
        self.bookManage.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 用户管理
        self.userManage = QToolButton()
        self.userManage.setText('用户管理')
        self.userManage.setFixedSize(160, 50)
        self.userManage.setIcon(QIcon('icon/detial.png'))
        self.userManage.setIconSize(QSize(30, 30))
        self.userManage.clicked.connect(lambda: self.switch(1, self.userManage))
        self.userManage.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 借阅日志
        self.history = QToolButton()
        self.history.setText('借阅日志')
        self.history.setFixedSize(160, 50)
        self.history.setIcon(QIcon('icon/history.png'))
        self.history.setIconSize(QSize(30, 30))
        self.history.clicked.connect(lambda: self.switch(2, self.history))
        self.history.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 借阅信息管理
        self.borrowManage = QToolButton()
        self.borrowManage.setText('借阅管理')
        self.borrowManage.setFixedSize(160, 50)
        self.borrowManage.setIcon(QIcon('icon/borrowing.png'))
        self.borrowManage.setIconSize(QSize(30, 30))
        self.borrowManage.clicked.connect(lambda: self.switch(3, self.borrowManage))
        self.borrowManage.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.btnList = [self.bookManage,
                        self.userManage, self.history, self.borrowManage]

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.bookManage)
        self.layout.addWidget(self.userManage)
        self.layout.addWidget(self.history)
        self.layout.addWidget(self.borrowManage)
        self.layout.addStretch()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.menu = QGroupBox()
        self.menu.setFixedSize(160, 500)
        self.menu.setLayout(self.layout)
        self.menu.setContentsMargins(0, 0, 0, 0)
        self.body.addWidget(self.menu)

    def switch(self, index, btn):
        self.focus = index
        for i in self.btnList:
            i.setStyleSheet('''
            *{
                background: white;
            }
            QToolButton:hover{
                background-color: rgba(230, 230, 230, 0.3);
            }
            ''')

        btn.setStyleSheet('''
        QToolButton{
            background-color: rgba(230, 230, 230, 0.7);
        }
        ''')
        self.setContent()

    # 设置右侧信息页
    def setContent(self):
        if self.content is not None:
            self.content.deleteLater()
        if self.focus == 0 or True:
            self.content = BookManage(self.stu_mes)
        # elif self.focus == 1:
        #     self.content = BorrowingBooks(self.stu_mes)
        # elif self.focus == 2:
        #     self.content = History(self.stu_mes)
        # else:
        #     self.content = Detial(self.stu_mes)
        self.body.addWidget(self.content)

    def setMyStyle(self):
        self.setStyleSheet('''
        QWidget{
            background-color: white;
        }
        ''')
        self.titleBar.setStyleSheet('''
        QWidget{
            background-color: rgba(44,44,44,1);
            border:1px solid black;
            border-radius: 10px;
        }
        ''')
        self.menu.setStyleSheet('''
        QWidget{
            border: 0px;
            border-right: 1px solid rgba(227, 227, 227, 1);
        }
        QToolButton{
            color: rgba(51, 90, 129, 1);
            font-family: 微软雅黑;
            font-size: 25px;
            border-right: 1px solid rgba(227, 227, 227, 1);
        }
        QToolButton:hover{
            background-color: rgba(230, 230, 230, 0.3);
        }
        ''')
        self.title.setStyleSheet('''
        *{
            color: white;
            font-family: 微软雅黑;
            font-size: 25px;
            border: 0px;
        }
        ''')
        self.account.setStyleSheet('''
        *{
            color: white;
            font-weight: 微软雅黑;
            font-size: 25px;
            border: 0px;
        }
        ''')
        self.out.setStyleSheet('''
        QToolButton{
            color: white;
            border:0px;
            font-size: 12px;
        }
        QToolButton:hover{
            color: rgba(11, 145, 255, 1);
        }
        ''')


class BookManage(QGroupBox):
    def __init__(self, stu_mes):
        super().__init__()
        self.stu_mes = stu_mes
        self.book_list = []
        self.body = QVBoxLayout()
        self.setTitleBar()
        self.setSearchBar()
        self.setTable()

        self.setLayout(self.body)
        self.initUI()

    # 标题栏
    def setTitleBar(self):
        self.title = QLabel()
        self.title.setText('书籍信息信息管理')
        self.title.setFixedHeight(25)
        titleLayout = QHBoxLayout()
        titleLayout.addSpacing(50)
        titleLayout.addWidget(self.title)
        self.titleBar = QWidget()
        self.titleBar.setFixedSize(900, 50)
        self.titleBar.setLayout(titleLayout)
        self.body.addWidget(self.titleBar)

    # 设置搜索框
    def setSearchBar(self):
        self.searchTitle = QLabel()
        self.searchTitle.setText('搜索书籍')
        self.searchInput = QLineEdit()
        self.searchInput.setText('ID/书名/作者/出版社')
        self.searchInput.setClearButtonEnabled(True)
        self.searchInput.setFixedSize(400, 40)
        self.searchButton = QToolButton()
        self.searchButton.setFixedSize(100, 40)
        self.searchButton.setText('搜索')
        self.searchButton.clicked.connect(self.searchFunction)
        self.addNewBookButton = QToolButton()
        self.addNewBookButton.setFixedSize(120, 40)       
        self.addNewBookButton.setText('插入新书')
        self.addNewBookButton.clicked.connect(self.addNewBookFunction)
        searchLayout = QHBoxLayout()
        searchLayout.addStretch()
        searchLayout.addWidget(self.searchTitle)
        searchLayout.addWidget(self.searchInput)
        searchLayout.addWidget(self.searchButton)
        searchLayout.addWidget(self.addNewBookButton)
        searchLayout.addStretch()
        self.searchWidget = QWidget()
        self.searchWidget.setLayout(searchLayout)
        self.body.addWidget(self.searchWidget)

    # 搜索方法
    def searchFunction(self):
        self.book_list = database.search_book(self.searchInput.text())
        if self.book_list == []:
            print('未找到')
        self.table.deleteLater()
        self.setTable()

    # 设置表格
    def setTable(self):
        self.table = QTableWidget(1, 8)
        self.table.setContentsMargins(10, 10, 10, 10)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        # self.table.setColumnWidth(0, 150)
        # self.table.setColumnWidth(1, 150)
        # self.table.setColumnWidth(2, 125)
        # self.table.setColumnWidth(3, 125)
        # self.table.setColumnWidth(4, 100)
        # self.table.setColumnWidth(5, 150)

        self.table.setItem(0, 0, QTableWidgetItem('书号'))
        self.table.setItem(0, 1, QTableWidgetItem('书名'))
        self.table.setItem(0, 2, QTableWidgetItem('作者'))
        self.table.setItem(0, 3, QTableWidgetItem('出版日期'))
        self.table.setItem(0, 4, QTableWidgetItem('出版社'))
        self.table.setItem(0, 5, QTableWidgetItem('位置'))
        self.table.setItem(0, 6, QTableWidgetItem('总数/剩余'))
        self.table.setItem(0, 7, QTableWidgetItem('操作'))

        for i in range(8):
            self.table.item(0, i).setTextAlignment(Qt.AlignCenter)
            self.table.item(0, i).setFont(QFont('微软雅黑', 15))

        # 显示借阅详情
        for i in self.book_list:
            self.insertRow(i)
        self.body.addWidget(self.table)

    # 插入行
    def insertRow(self, val: list):
        itemBID = QTableWidgetItem(val[0])
        itemBID.setTextAlignment(Qt.AlignCenter)

        itemNAME = QTableWidgetItem('《' + val[1] + '》')
        itemNAME.setTextAlignment(Qt.AlignCenter)

        itemAUTHOR = QTableWidgetItem(val[2])
        itemAUTHOR.setTextAlignment(Qt.AlignCenter)

        itemDATE = QTableWidgetItem(val[3])
        itemDATE.setTextAlignment(Qt.AlignCenter)

        itemPRESS = QTableWidgetItem(val[4])
        itemPRESS.setTextAlignment(Qt.AlignCenter)

        itemPOSITION = QTableWidgetItem(val[5])
        itemPOSITION.setTextAlignment(Qt.AlignCenter)

        itemSUM = QTableWidgetItem(str(val[6])+'/'+str(val[7]))
        itemSUM.setTextAlignment(Qt.AlignCenter)

        itemModify = QToolButton(self.table)
        itemModify.setFixedSize(50, 25)
        itemModify.setText('修改')
        itemModify.clicked.connect(lambda: self.updateBookFunction(val[0]))
        itemModify.setStyleSheet('''
        *{
            color: white;
            font-family: 微软雅黑;
            background: rgba(38, 175, 217, 1);
            border: 0;
            border-radius: 10px;
        }
        ''')
        itemDelete = QToolButton(self.table)
        itemDelete.setFixedSize(50, 25)
        itemDelete.setText('删除')
        itemDelete.setEnabled(False)
        itemDelete.setStyleSheet('''
        *{
            color: white;
                font-family: 微软雅黑;
                background: rgba(222, 52, 65, 1);
                border: 0;
                border-radius: 10px;
        }
        ''')

        itemLayout = QHBoxLayout()
        itemLayout.setContentsMargins(0, 0, 0, 0)
        itemLayout.addWidget(itemModify)
        itemLayout.addWidget(itemDelete)
        itemWidget = QWidget()
        itemWidget.setLayout(itemLayout)

        self.table.insertRow(1)
        self.table.setItem(1, 0, itemBID)
        self.table.setItem(1, 1, itemNAME)
        self.table.setItem(1, 2, itemAUTHOR)
        self.table.setItem(1, 3, itemDATE)
        self.table.setItem(1, 4, itemPRESS)
        self.table.setItem(1, 5, itemPOSITION)
        self.table.setItem(1, 6, itemSUM)
        self.table.setCellWidget(1, 7, itemWidget)

    def updateBookFunction(self, BID: str):
        book_info = database.get_book_info(BID)
        if book_info is None:
            return
        self.sum = book_info['SUM']
        self.updateBookDialog = book_information.BookInfo(book_info)
        self.updateBookDialog.after_close.connect(self.updateBook)
        self.updateBookDialog.show()

    def updateBook(self, book_info: dict):
        change = self.sum - book_info['SUM']
        # 书本减少的数量不能大于未借出的书本数
        if change > book_info['NUM']:
            book_info['SUM'] = self.sum - book_info['NUM']
            book_info['NUM'] = 0
        else:
            book_info['NUM'] -= change
        ans = database.update_book(book_info)
        if ans:
            self.searchFunction()

    def addNewBookFunction(self):
        self.newBookDialog = book_information.BookInfo()
        self.newBookDialog.show()
        self.newBookDialog.after_close.connect(self.addNewBook)

    def addNewBook(self, book_info: dict):
        ans = database.new_book(book_info)
        if ans:
            self.searchFunction()

    def initUI(self):
        self.setFixedSize(1100, 600)
        self.setStyleSheet('''
        *{
            background-color: white;
            border:0px;
        }
        ''')
        self.titleBar.setStyleSheet('''
        QWidget {
            border:0;
            background-color: rgba(216, 216, 216, 1);
            border-radius: 20px;
            color: rgba(113, 118, 121, 1);
        }
        QLabel{
            font-size: 25px;
            font-family: 微软雅黑;
        }
        ''')
        self.searchTitle.setStyleSheet('''
            QLabel{
                font-size:20px;
                color: black;
                font-family: 微软雅黑;
            }
        ''')
        self.searchInput.setStyleSheet('''
            QLineEdit{
                border: 1px solid rgba(201, 201, 201, 1);
                border-radius: 5px;
                color: rgba(120, 120, 120, 1)
            }
        ''')
        self.searchButton.setStyleSheet('''
            QToolButton{
                border-radius: 10px;
                background-color:rgba(52, 118, 176, 1);
                color: white;
                font-size: 25px;
                font-family: 微软雅黑;
            }
        ''')
        self.addNewBookButton.setStyleSheet('''
            QToolButton{
                border-radius: 10px;
                background-color:rgba(52, 118, 176, 1);
                color: white;
                font-size: 25px;
                font-family: 微软雅黑;
            }
        ''')
        self.table.setStyleSheet('''
            font-size:18px;
            color: black;
            background-color: white;
            font-family: 微软雅黑;
        ''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_message = {
        'class': 'admin',
        'AID': 'admin'
    }
    ex = AdministratorPage(user_message)
    ex.show()
    sys.exit(app.exec_())
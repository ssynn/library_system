import sys
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QLabel, QLineEdit, QToolButton, QGroupBox)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

KEY_LIST = ['BID', 'BNAME', 'AUTHOR',
            'PUBLICATION_DATE', 'PRESS', 'POSITION', 'SUM', 'CLASSIFICATION']


class BookInfo(QGroupBox):
    '''
    编辑书本信息的界面
    返回book_msg{
        'BID': str,
        'BNAME': str,
        'AUTHOR': str,
        'PUBLICATION_DATE': str,
        'PRESS': str,
        'POSITION': str,
        'SUM': int,
        'CLASSIFICATION': str
    }
    '''
    after_close = pyqtSignal(dict)

    def __init__(self, book_msg: dict = None):
        super().__init__()
        if book_msg is not None:
            self.book_msg = book_msg
        else:
            self.book_msg = {
                'BID': '请输入书号',
                'BNAME': '请输入书名',
                'AUTHOR': '请输入作者',
                'PUBLICATION_DATE': '请输入出版日期',
                'PRESS': '请输入出版社',
                'POSITION': '请输入存放位置',
                'SUM': '请输入数量',
                'CLASSIFICATION': '请输入分类, 以空格区分'
            }

        self.title = QLabel()
        self.title.setText('书本信息')

        self.subTitle = QLabel()
        self.subTitle.setText('编辑书籍信息')

        # 书号输入框
        self.BIDInput = QLineEdit()
        self.BIDInput.setFixedSize(400, 40)
        self.BIDInput.setText(self.book_msg['BID'])
        self.BIDInput.initText = '请输入书号'
        self.BIDInput.mousePressEvent = lambda x: self.inputClick(self.BIDInput)
        # BID不允许修改
        if self.BIDInput.text() != self.BIDInput.initText:
            self.BIDInput.setEnabled(False)

        # 书名输入框
        self.BNAMEInput = QLineEdit()
        self.BNAMEInput.setFixedSize(400, 40)
        self.BNAMEInput.setText(self.book_msg['BNAME'])
        self.BNAMEInput.initText = '请输入书名'
        self.BNAMEInput.mousePressEvent = lambda x: self.inputClick(self.BNAMEInput)

        # 总书数
        self.NumInput = QLineEdit()
        self.NumInput.setFixedSize(400, 40)
        self.NumInput.setText(str(self.book_msg['SUM']))
        self.NumInput.initText = '请输入数量'
        self.NumInput.mousePressEvent = lambda x: self.inputClick(self.NumInput)

        # 作者
        self.AUTHORInput = QLineEdit()
        self.AUTHORInput.setFixedSize(400, 40)
        self.AUTHORInput.setText(self.book_msg['AUTHOR'])
        self.AUTHORInput.initText = '请输入作者'
        self.AUTHORInput.mousePressEvent = lambda x: self.inputClick(self.AUTHORInput)

        # 出版社
        self.PRESSInput = QLineEdit()
        self.PRESSInput.setFixedSize(400, 40)
        self.PRESSInput.setText(self.book_msg['PRESS'])
        self.PRESSInput.initText = '请输入出版社'
        self.PRESSInput.mousePressEvent = lambda x: self.inputClick(self.PRESSInput)

        # 出版日期
        self.DATEInput = QLineEdit()
        self.DATEInput.setFixedSize(400, 40)
        self.DATEInput.setText(self.book_msg['PUBLICATION_DATE'])
        self.DATEInput.initText = '请输入出版日期'
        self.DATEInput.mousePressEvent = lambda x: self.inputClick(self.DATEInput)

        # 位置
        self.POSITIONInput = QLineEdit()
        self.POSITIONInput.setFixedSize(400, 40)
        self.POSITIONInput.setText(self.book_msg['POSITION'])
        self.POSITIONInput.initText = '请输入存放位置'
        self.POSITIONInput.mousePressEvent = lambda x: self.inputClick(self.POSITIONInput)

        # 分类
        self.CLASSIFICATIONInput = QLineEdit()
        self.CLASSIFICATIONInput.setFixedSize(400, 40)
        self.CLASSIFICATIONInput.setText(self.book_msg['CLASSIFICATION'])
        self.CLASSIFICATIONInput.initText = '请输入分类, 以空格区分'
        self.CLASSIFICATIONInput.mousePressEvent = lambda x: self.inputClick(self.CLASSIFICATIONInput)

        # 提交
        self.submit = QToolButton()
        self.submit.setText('提交')
        self.submit.setFixedSize(400, 40)
        self.submit.clicked.connect(self.submitFunction)

        # 退出
        self.back = QToolButton()
        self.back.setText('退出')
        self.back.setFixedSize(400, 40)
        self.back.clicked.connect(self.close)

        self.btnList = [
            self.BIDInput,
            self.BNAMEInput,
            self.AUTHORInput,
            self.DATEInput,
            self.PRESSInput,
            self.POSITIONInput,
            self.NumInput,
            self.CLASSIFICATIONInput
        ]

        self.bodyLayout = QVBoxLayout()
        self.bodyLayout.addWidget(self.title)
        self.bodyLayout.addWidget(self.subTitle)
        for i in self.btnList:
            self.bodyLayout.addWidget(i)
        self.bodyLayout.addWidget(self.submit)
        self.bodyLayout.addWidget(self.back)

        self.setLayout(self.bodyLayout)
        self.initUI()

    def inputClick(self, e):
        for item in self.btnList:
            if item.text() == '':
                item.setText(item.initText)
        if e.text() == e.initText:
            e.setText('')

    def submitFunction(self):
        for btn, key in zip(self.btnList, KEY_LIST):
            if btn.text() == btn.initText:
                self.book_msg[key] = ''
            else:
                self.book_msg[key] = btn.text()
        if self.book_msg['SUM'].isalnum():
            self.book_msg['SUM'] = int(self.book_msg['SUM'])
        else:
            self.book_msg['SUM'] = 0
        self.close()
        self.after_close.emit(self.book_msg)

    def initUI(self):
        self.setFixedSize(422, 550)
        self.setWindowTitle('编辑书本')
        self.setWindowIcon(QIcon('icon/book.png'))
        self.setMyStyle()

    def setMyStyle(self):
        self.setStyleSheet('''
        QWidget{
            background-color: white;
        }
        QLineEdit{
            border:0px;
            border-bottom: 1px solid rgba(229, 229, 229, 1);
            color: grey;
        }
        QToolButton{
            border: 0px;
            background-color:rgba(52, 118, 176, 1);
            color: white;
            font-size: 25px;
            font-family: 微软雅黑;
        }
        QGroupBox{
            border: 1px solid rgba(229, 229, 229, 1);
            border-radius: 5px;
        }
        ''')
        self.title.setStyleSheet('''
        *{
            color: rgba(113, 118, 121, 1);
            font-size: 30px;
            font-family: 微软雅黑;
        }
        ''')
        self.subTitle.setStyleSheet('''
        *{
            color: rgba(184, 184, 184, 1);
        }
        ''')


if __name__ == '__main__':
    book_msg = {
                'BID': '4',
                'BNAME': 'Java',
                'AUTHOR': 'kak',
                'PUBLICATION_DATE': '2009-05',
                'PRESS': '电子出版社',
                'POSITION': 'C05',
                'SUM': 5,
                'CLASSIFICATION': 'aasd asd asd ad '
            }
    app = QApplication(sys.argv)
    ex = BookInfo(book_msg)
    ex.show()
    sys.exit(app.exec_())

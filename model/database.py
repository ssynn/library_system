'''
所有有关数据库的操作全部集中在这个文件中
'''
import time
import pymssql


CONFIG = {
    "host": '127.0.0.1:1433',
    "user": 'sa',
    "pwd": '123456',
    'db': 'Library'
}


def remove_zero(val):
    while len(val) != 0 and val[-1] == ' ':
        val = val[:-1]
    return val


# 将元组列表转换为字典
def convert(val: list):
    if len(val) == 0:
        return None
    val = val[0]
    # 如果是学生
    if len(val) == 5:
        ans = {
            'class': 'stu',
            'SID': remove_zero(val[0]),
            'SNAME': remove_zero(val[1]),
            'DEPARTMENT': remove_zero(val[2]),
            'MAJOR': remove_zero(val[3]),
            'MAX': val[4]
        }
    else:
        ans = {
            'class': 'admin',
            'AID': remove_zero(val[0])
        }
    return ans


# 将日期延后两个月
def postpone(start: str):
    temp = start.split('-')
    temp[0] = int(temp[0])
    temp[1] = int(temp[1])
    temp[1] += 2
    if temp[1] > 12:
        temp[1] -= 12
        temp[0] += 1
    ans = '{:d}-{:0>2d}-{}-{}'.format(temp[0], temp[1], temp[2], temp[3])
    return ans


def signup(user_message: dict) -> bool:
    '''
    user_message should be in the following formate
    user_message{
        'SID': str,
        'PASSWORD': str,
        'SNAME': str,
        'DEPARTMENT': str,
        'MAJOR': str,
        'MAX': int
    }
    '''
    res = True
    try:
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        cursor.execute('''
            SELECT *
            FROM student
            WHERE SID=%s
            ''', (user_message['SID']))
        if len(cursor.fetchall()) != 0:
            raise Exception('用户已存在!')
        cursor.execute('''
        INSERT
        INTO student
        VALUES(%s, %s, %s, %s, %s, %d)
        ''', (
            user_message['SID'],
            user_message['PASSWORD'],
            user_message['SNAME'],
            user_message['DEPARTMENT'],
            user_message['MAJOR'],
            user_message['MAX']
        ))
        conn.commit()
    except Exception as e:
        print('Signup error!')
        print(e)
        res = False
    finally:
        conn.close()
        return res


def signin(user_message: dict) -> dict:
    '''
    传入以下格式的字典
    user_message{
        'ID': str,
        'PASSWORD': str
    }
    如果管理员用户存在返回以下字典
    {
        'class': 'admin'
        'AID': str
    }
    如果学生用户存在返回以下格式的字典
    {
        'class': 'stu'
        'SID': str,
        'SNAME': str,
        'DEPARTMENT': str,
        'MAJOR': str,
        'MAX': int
    }
    否则返回None
    '''
    ans = None
    try:
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        # 现在administrator表内匹配
        cursor.execute('''
        SELECT AID
        FROM administrator
        WHERE AID=%s AND PASSWORD=%s
        ''', (
            user_message['ID'],
            user_message['PASSWORD']
        ))
        temp = cursor.fetchall()
        # 管理员表内没有找到则在student表内匹配
        if len(temp) == 0:
            cursor.execute('''
            SELECT SID, SNAME, DEPARTMENT, MAJOR, MAX
            FROM student
            WHERE SID=%s AND PASSWORD=%s
            ''', (
                user_message['ID'],
                user_message['PASSWORD']
            ))
            temp = cursor.fetchall()
        ans = temp
        conn.commit()
    except Exception as e:
        print('Signin error!')
        print(e)
    finally:
        conn.close()
        return convert(ans)


def update_student(user_message):
    '''
    user_message should be in the following formate
    user_message{
        'SID': str,
        'PASSWORD': str,
        'SNAME': str,
        'DEPARTMENT': str,
        'MAJOR': str,
        'MAX': int
    }
    '''
    pass


def find_student(mes: str) -> dict:
    '''
    可传入学生是学号或姓名进行查找
    '''
    pass


def get_borrowing_books(SID: str) -> list:
    '''
    传入学生学号，返回此学生在借的书籍列表信息
    [[BID, BNAME, BORROW_DATE, DEADLINE, PUNISH, NUM],[...],....]
    '''
    try:
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        cursor.execute('''
        SELECT book.BID, BNAME, BORROW_DATE, DEADLINE, PUNISH, NUM
        FROM borrowing_book, book
        WHERE SID=%s AND book.BID=borrowing_book.BID
        ''', (SID,))
        res = cursor.fetchall()
    except Exception as e:
        print('Signup error!')
        print(e)
        res = []
    finally:
        conn.close()
        temp = []
        for i in res:
            temp_ = []
            for j in range(4):
                temp_.append(remove_zero(i[j]))
            temp_.append(i[4])
            temp_.append(i[5])
            temp.append(temp_)
        return temp


def return_book(BID: str, SID: str) -> bool:
    '''
    传入BID, SID，删除borrowing_book表内的记录在log表内新建记录
    返回bool型
    '''
    try:
        res = True
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        # 先把借书日期，书本剩余数量，罚金等信息找出
        cursor.execute('''
        SELECT BORROW_DATE, NUM, PUNISH
        FROM book, borrowing_book
        WHERE SID=%s AND borrowing_book.BID=%s AND borrowing_book.BID=book.BID
        ''', (SID, BID))
        book_mes = cursor.fetchall()
        NUM = book_mes[0][1]
        BORROW_DATE = book_mes[0][0]
        PUNISH = book_mes[0][2]
        BACK_DATE = time.strftime("%Y-%m-%d-%H:%M")

        # book表内NUM加一，删除borrowing_book表内的记录，把记录插入log表
        cursor.execute('''
        UPDATE book
        SET NUM=%d
        WHERE BID=%s
        DELETE
        FROM borrowing_book
        WHERE SID=%s AND BID=%s
        INSERT
        INTO log
        VALUES(%s, %s, %s, %s, %d)
        ''', (NUM+1, BID, SID, BID, BID, SID, BORROW_DATE, BACK_DATE, PUNISH))
        conn.commit()
    except Exception as e:
        print('Return error!')
        print(e)
        res = False
    finally:
        conn.close()
        return res


def delete_student(SID: str) -> bool:
    pass


def new_book(book_message: dict) -> bool:
    pass


def update_book(book_message: dict) -> bool:
    pass


def delete_book(BID: str) -> bool:
    pass


def search_book(mes: str, stu_mes: dict = {'SID': '1', 'MAX': 5}) -> list:
    '''
    可以传入BID或作者或出版或书名社进行查找
    返回[[BID, BNAME, AUTHOR, PUBLICATION_DATE, PRESS, POSITION, SUM, NUM, STATE],...]
    '''
    try:
        res = []
        val = mes.split()
        val = [('%'+i+'%', i, '%'+i+'%', '%'+i+'%') for i in val]
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()

        # 显示所有书信息
        if mes == 'ID/书名/作者/出版社':
            cursor.execute('''
            SELECT *
            FROM book
            ''')
        else:
            # 先把借书日期，书本剩余数量，罚金等信息找出
            cursor.executemany('''
            SELECT *
            FROM book
            WHERE PRESS LIKE %s OR BID=%s OR BNAME LIKE %s OR AUTHOR LIKE %s
            ''', val)

        res = cursor.fetchall()
        temp = []
        for i in res:
            temp_ = []
            for j in range(6):
                temp_.append(remove_zero(i[j]))
            temp_.append(i[6])
            temp_.append(i[7])
            temp.append(temp_)
        res = temp

        # 匹配学生信息
        punish = False
        borrowing_book = get_borrowing_books(stu_mes['SID'])
        for i in borrowing_book:
            if i[3] < time.strftime("%Y-%m-%d-%H:%M"):
                punish = True
                break
        for book in res:
            # 有罚金没交
            if punish:
                book.append('未交罚金')
                continue
            # 如果已经借的书达到上限就不再可借
            if len(borrowing_book) >= stu_mes['MAX']:
                book.append('借书达上限')
                continue
            # 判断受否有此书
            for borrow in borrowing_book:
                if book[0] == borrow[0]:
                    book.append('已借此书')
                    break
            if book[-1] != '已借此书':
                book.append('借书')

    except Exception as e:
        print('Search error!')
        print(e)
        res = []
    finally:
        conn.close()
        return res


# 借书
def borrow_book(BID: str, SID: str):
    '''
    传入BID和SID
    返回bool
    book的NUM减一
    在borrowing_book表内新建记录
    '''
    try:
        res = True
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        # 先把借书日期，书本剩余数量，罚金等信息找出
        cursor.execute('''
        SELECT NUM
        FROM book
        WHERE BID=%s
        ''', (BID))
        book_mes = cursor.fetchall()
        # print(book_mes)
        NUM = book_mes[0][0]
        BORROW_DATE = time.strftime("%Y-%m-%d-%H:%M")
        DEADLINE = postpone(BORROW_DATE)

        # book表内NUM减一，新建borrowing_book表内的记录
        cursor.execute('''
        UPDATE book
        SET NUM=%d
        WHERE BID=%s
        INSERT
        INTO borrowing_book
        VALUES(%s, %s, %s, %s, 0)
        ''', (NUM-1, BID, BID, SID, BORROW_DATE, DEADLINE))
        conn.commit()

    except Exception as e:
        print('borrow error!')
        print(e)
        res = False
    finally:
        conn.close()
        return res


if __name__ == '__main__':
    temp = {
        'SID': '201602',
        'PASSWORD': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
        'SNAME': '小王',
        'DEPARTMENT': '数学与信息科学学院',
        'MAJOR': 'SE',
        'MAX': 5,
        'PUNISHED': 0
    }
    temp_login = {
        'ID': '1',
        'PASSWORD': '4fc82b26aecb47d2868c4efbe3581732a3e7cbcc6c2efb32062c08170a05eeb8'
    }
    # print(signup(temp))
    # print(get_borrowing_books('1'))
    # print(return_book('0001', '1'))
    # print(get_borrowing_books('1'))
    # print(signin(temp_login))
    print(search_book('ID/书名/作者/出版社'))
    # print(postpone('2018-11-10-10:58'))
    # print(borrow_book('2', '1'))

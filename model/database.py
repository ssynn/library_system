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


# 去掉字符串末尾的0
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


# 把书的元组列表转换为字典
def convert_book(val: tuple) -> dict:
    key_list = ['BID', 'BNAME', 'AUTHOR', 'PUBLICATION_DATE', 'PRESS', 'POSITION', 'SUM', 'NUM']
    ans = {}
    for i, key in zip(val, key_list):
        ans[key] = i
        if type(i) is not int:
            ans[key] = remove_zero(i)
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


# 两个日期之间间隔的天数
def days_between(start: str, end: str):
    start = start.split('-')
    end = end.split('-')
    start[0] = int(start[0])
    start[1] = int(start[1])
    start[2] = int(start[2])

    end[0] = int(end[0])
    end[1] = int(end[1])
    end[2] = int(end[2])

    s = start[0]*365+start[1]*30+start[2]
    e = end[0]*365+end[1]*30+end[2]
    return e-s


# 注册
def signup(user_message: dict) -> bool:
    '''
    传入以下格式的字典
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


# 登录
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


# 更新学生信息
def update_student(user_message: dict) -> bool:
    '''
    传入字典格式如下
    user_message{
        'SID': str,
        'PASSWORD': str,
        'SNAME': str,
        'DEPARTMENT': str,
        'MAJOR': str,
        'MAX': int
    }
    返回bool
    '''
    try:
        res = True
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE student
            SET SNAME=%s, DEPARTMENT=%s, MAJOR=%s, MAX=%s
            WHERE SID=%s
            ''', (
                user_message['SNAME'],
                user_message['DEPARTMENT'],
                user_message['MAJOR'],
                user_message['MAX'],
                user_message['SID']
            ))
        if 'PASSWORD' in user_message:
            cursor.execute('''
            UPDATE student
            SET PASSWORD=%s
            WHERE SID=%s
            ''', (
                user_message['PASSWORD'],
                user_message['SID']
            ))
        conn.commit()
    except Exception as e:
        print('Update error!')
        print(e)
        res = False
    finally:
        conn.close()
        return res


# 获取学生信息
def get_student_info(SID: str) -> dict:
    '''
    传入SID
    返回stu_info{
        'class': stu,
        'SID': str,
        'SNAME': str,
        'DEPARTMENT': str,
        'MAJOR': str,
        'MAX': int
    }
    '''
    try:
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SID, SNAME, DEPARTMENT, MAJOR, MAX
            FROM student
            WHERE SID=%s
            ''', (SID))
        ans = cursor.fetchall()
    except Exception as e:
        print(e)
        print('get student info error')
    finally:
        conn.close()
        return convert(ans)


# 查找学生
def search_student(info: str):
    '''
    传入SID或学生姓名进行查找
    返回[[SID, SNAME, DEPARTMENT, MAJOR, MAX],...]
    '''
    try:
        res = []
        val = info.split()
        val = [(i, '%'+i+'%') for i in val]
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        # 显示所有书信息
        if info == 'ID/姓名' or info == '':
            cursor.execute('''
            SELECT SID, SNAME, DEPARTMENT, MAJOR, MAX
            FROM student
            ''')
            res += cursor.fetchall()
        else:
            # 按条件查找
            for i in val:
                cursor.execute('''
                SELECT SID, SNAME, DEPARTMENT, MAJOR, MAX
                FROM student
                WHERE SID=%s OR SNAME LIKE %s
                ''', i)
                res += cursor.fetchall()
        res = list(set(res))
        temp = []
        for i in res:
            temp_ = []
            for j in range(4):
                temp_.append(remove_zero(i[j]))
            temp_.append(i[4])
            temp.append(temp_)
        res = temp
    except Exception as e:
        print('Search student error!')
        print(e)
        res = []
    finally:
        conn.close()
        return res


# 删除学生信息
def delete_student(SID: str) -> bool:
    '''
    传入SID
    删除student表内记录, 
    找出book表内所借的书强制还书
    删除log表内的记录
    '''
    try:
        res = True
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        # 先强制把书还掉
        cursor.execute('''
            SELECT BID
            FROM borrowing_book
            WHERE SID=%s
        ''', (SID))
        BID_list = cursor.fetchall()
        for BID in BID_list:
            return_book(BID, SID)
        # 再删除学生信息
        cursor.execute('''
            DELETE
            FROM student
            WHERE SID=%s
            DELETE
            FROM log
            WHERE SID=%s
            ''', (SID, SID))
        conn.commit()
    except Exception as e:
        print('delete book error!')
        print(e)
        res = False
    finally:
        conn.close()
        return res


# 获取学生的借书信息
def get_borrowing_books(ID: str, BID: bool = False) -> list:
    '''
    当BID为False
    传入学SID，返回此学生在借的书籍列表信息
    [[BID, BNAME, BORROW_DATE, DEADLINE, PUNISH, NUM],[...],....]
    当BID=True
    传入BID，返回借此书的书籍列表信息
    [[BID, SID, BORROW_DATE, DEADLINE, PUNISH],...]
    '''
    try:
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        if ID == '' or ID == 'ID/姓名':
            cursor.execute('''
                SELECT *
                FROM borrowing_book
            ''')
            res = cursor.fetchall()
            temp = []
            for i in res:
                temp_ = []
                for j in range(4):
                    temp_.append(remove_zero(i[j]))
                temp_.append(i[4])
                temp.append(temp_)
        elif BID:
            cursor.execute('''
                SELECT *
                FROM borrowing_book
                WHERE BID=%s
            ''', (ID,))
            res = cursor.fetchall()
            temp = []
            for i in res:
                temp_ = []
                for j in range(4):
                    temp_.append(remove_zero(i[j]))
                temp_.append(i[4])
                temp.append(temp_)
        else:
            cursor.execute('''
                SELECT book.BID, BNAME, BORROW_DATE, DEADLINE, PUNISH, NUM
                FROM borrowing_book, book
                WHERE SID=%s AND book.BID=borrowing_book.BID
            ''', (ID,))
            res = cursor.fetchall()
            temp = []
            for i in res:
                temp_ = []
                for j in range(4):
                    temp_.append(remove_zero(i[j]))
                temp_.append(i[4])
                temp_.append(i[5])
                temp.append(temp_)
        res = temp
    except Exception as e:
        print('get borrowing books error!')
        print(e)
        res = []
    finally:
        conn.close()
        return temp


# 还书
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


# 交罚金
def pay(BID: str, SID: str, PUNISH: int) -> bool:
    '''
    传入BID, SID, PUNISH把当前数的DEADLINE往后延长两个月
    返回bool型
    '''
    try:
        res = True
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()

        # book表内NUM加一，删除borrowing_book表内的记录，把记录插入log表
        cursor.execute('''
            UPDATE borrowing_book
            SET DEADLINE=%s, PUNISH=%d
            WHERE BID=%s AND SID=%s
            ''', (postpone(time.strftime('%Y-%m-%d-%H:%M')), PUNISH, BID, SID))
        conn.commit()
    except Exception as e:
        print('Pay error!')
        print(e)
        res = False
    finally:
        conn.close()
        return res


# 获取历史记录
def get_log(SID: str) -> list:
    '''
    传入SID
    返回[[BID, BNAME, BORROW_DATE, BACK_DATE, PUNISHED],...]
    '''
    try:
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        cursor.execute('''
        SELECT book.BID, BNAME, BORROW_DATE, BACK_DATE, PUNISHED
        FROM log, book
        WHERE SID=%s AND book.BID=log.BID
        ''', (SID,))
        res = cursor.fetchall()
    except Exception as e:
        print('get log error!')
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
            temp.append(temp_)
        temp.sort(key=lambda x: x[3])
        return temp


# 加入新书
def new_book(book_info: dict) -> bool:
    '''
    传入以下格式的字典
    book_msg{
        'BID': str,
        'BNAME': str,
        'AUTHOR': str,
        'PUBLICATION_DATE': str,
        'PRESS': str,
        'POSITION': str,
        'SUM': int
    }
    返回bool
    '''
    res = True
    try:
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        cursor.execute('''
            SELECT *
            FROM book
            WHERE BID=%s
            ''', (book_info['BID']))
        if len(cursor.fetchall()) != 0:
            raise Exception('书ID已存在!')
        cursor.execute('''
        INSERT
        INTO book
        VALUES(%s, %s, %s, %s, %s, %s, %d, %d)
        ''', (
            book_info['BID'],
            book_info['BNAME'],
            book_info['AUTHOR'],
            book_info['PUBLICATION_DATE'],
            book_info['PRESS'],
            book_info['POSITION'],
            book_info['SUM'],
            book_info['SUM']
        ))
        conn.commit()
    except Exception as e:
        print('add book error!')
        print(e)
        res = False
    finally:
        conn.close()
        return res


# 获取新书详细信息
def get_book_info(BID: str) -> dict:
    '''
    传入BID
    返回book_msg{
        'BID': str,
        'BNAME': str,
        'AUTHOR': str,
        'PUBLICATION_DATE': str,
        'PRESS': str,
        'POSITION': str,
        'SUM': int,
        'NUM': int
    }
    '''
    try:
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        cursor.execute('''
            SELECT *
            FROM book
            WHERE BID=%s
            ''', (BID))
        res = cursor.fetchall()
        if len(res) == 0:
            raise Exception('查无此书')
    except Exception as e:
        print('get book info error!')
        print(e)
        res = None
    finally:
        conn.close()
        if res is not None:
            res = convert_book(res[0])
        return res


# 更新书籍信息
def update_book(book_info: dict) -> bool:
    '''
    传入以下格式的字典
    book_msg{
        'BID': str,
        'BNAME': str,
        'AUTHOR': str,
        'PUBLICATION_DATE': str,
        'PRESS': str,
        'POSITION': str,
        'SUM': int,
        'NUM': int
    }
    返回bool
    '''
    try:
        res = True
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE book
            SET BNAME=%s, AUTHOR=%s, PUBLICATION_DATE=%s, PRESS=%s, POSITION=%s, SUM=%d, NUM=%d
            WHERE BID=%s
            ''', (
                book_info['BNAME'],
                book_info['AUTHOR'],
                book_info['PUBLICATION_DATE'],
                book_info['PRESS'],
                book_info['POSITION'],
                book_info['SUM'],
                book_info['NUM'],
                book_info['BID']
            ))
        conn.commit()
    except Exception as e:
        print('Update book error!')
        print(e)
        res = False
    finally:
        conn.close()
        return res


# 删除书籍
def delete_book(BID: str) -> bool:
    '''
    传入BID
    返回bool
    会删除book，borrowing_book，log表内所有对应的记录
    '''
    try:
        res = True
        conn = pymssql.connect(CONFIG['host'], CONFIG['user'], CONFIG['pwd'], CONFIG['db'])
        cursor = conn.cursor()
        cursor.execute('''
            DELETE
            FROM book
            WHERE BID=%s
            DELETE
            FROM borrowing_book
            WHERE BID=%s
            DELETE
            FROM log
            WHERE BID=%s
            ''', (BID, BID, BID))
        conn.commit()
    except Exception as e:
        print('delete book error!')
        print(e)
        res = False
    finally:
        conn.close()
        return res


# 搜索书籍
def search_book(mes: str, SID: str = '') -> list:
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
        if mes == 'ID/书名/作者/出版社' or mes == '':
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

        # 匹配学生信息判断每一本书是否可借
        if SID != '':
            cursor.execute('''
            SELECT MAX
            FROM student
            WHERE SID=%s
            ''', (SID))
            max_num = cursor.fetchall()[0][0]
            punish = False
            borrowing_book = get_borrowing_books(SID)
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
                if len(borrowing_book) >= max_num:
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
def borrow_book(BID: str, SID: str) -> bool:
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


# 密码   为了调试方便就先不加密了
def encrypt(val):
    import hashlib
    h = hashlib.sha256()
    password = val
    h.update(bytes(password, encoding='UTF-8'))
    result = h.hexdigest()
    result = val
    return result


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
    user_message = {
        'SID': '1',
        'SNAME': '1',
        'PASSWORD': '123456',
        'DEPARTMENT': '1',
        'MAJOR': '2',
        'MAX': 5
    }
    temp_login = {
        'ID': '1',
        'PASSWORD': '4fc82b26aecb47d2868c4efbe3581732a3e7cbcc6c2efb32062c08170a05eeb8'
    }
    book_msg = {
                'BID': '4',
                'BNAME': 'Java',
                'AUTHOR': 'kak',
                'PUBLICATION_DATE': '2009-05',
                'PRESS': '电子出版社',
                'POSITION': 'C05',
                'SUM': 5
            }
    # 注册测试
    # print(signup(temp))

    # 还书测试
    print(get_borrowing_books('1', False))
    # print(return_book('0001', '1'))
    # print(get_borrowing_books('1'))

    # 登录测试
    # print(signin(temp_login))

    # 查书测试
    # print(search_book('ID/书名/作者/出版社'))

    # 推迟日期方法测试
    # print(postpone('2018-11-10-10:58'))

    # 借书测试
    # print(borrow_book('2', '1'))

    # 获取借书日志测试
    # print(get_log('1'))

    # 更新学生信息测试
    # print(update_student(user_message))

    # 加入新书测试
    # print(new_book(book_msg))

    # 获取书本详细信息
    # print(get_book_info('7'))

    # 删除书籍
    # print(delete_book('3'))

    # 查找学生
    # print(search_student('a 1'))

    # 获取学生信息
    # print(get_student_info('1'))

    # 删除学生
    print(delete_student('3'))

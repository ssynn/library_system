'''
所有有关数据库的操作全部集中在这个文件中
'''

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
    if len(val) == 6:
        ans = {
            'class': 'stu',
            'SID': remove_zero(val[0]),
            'SNAME': remove_zero(val[1]),
            'DEPARTMENT': remove_zero(val[2]),
            'MAJOR': remove_zero(val[3]),
            'MAX': val[4],
            'PUNISHED': val[5]
        }
    else:
        ans = {
            'class': 'admin',
            'AID': remove_zero(val[0])
        }
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
        'MAX': int,
        'PUNISHED': int
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
        VALUES(%s, %s, %s, %s, %s, %d, %d)
        ''', (
            user_message['SID'],
            user_message['PASSWORD'],
            user_message['SNAME'],
            user_message['DEPARTMENT'],
            user_message['MAJOR'],
            user_message['MAX'],
            user_message['PUNISHED']
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
        'MAX': int,
        'PUNISHED': int
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
            SELECT SID, SNAME, DEPARTMENT, MAJOR, MAX, PUNISHED
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
        'MAX': int,
        'PUNISHED': int
    }
    '''
    pass


def find_student(mes: str) -> dict:
    '''
    可传入学生是学号或姓名进行查找
    '''
    pass


def delete_student(SID: str) -> bool:
    pass


def new_book(book_message: dict) -> bool:
    pass


def update_book(book_message: dict) -> bool:
    pass


def delete_book(BID: str) -> bool:
    pass


def find_book(mes: str) -> dict:
    '''
    可以传入BID或作者或出版社进行查找
    '''
    pass


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
        'ID': 'ssynn',
        'PASSWORD': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    }
    print(signup(temp))

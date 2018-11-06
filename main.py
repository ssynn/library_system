import pymssql
import time

CONFIG = {
    "host": '127.0.0.1:1433',
    "user": 'sa',
    "pwd": '123456',
    'db': 'Library'
}


def init_database(user: dict):
    conn = pymssql.connect(user['host'], user['user'], user['pwd'])
    cursor = conn.cursor()
    conn.autocommit(True)
    cursor.execute('''CREATE DATABASE Library''')
    conn.autocommit(False)
    cursor.execute('''
    USE Library
    CREATE TABLE student(
        SID char(15) PRIMARY KEY,
        PASSWORD char(70),
        SNAME ntext,
        DEPARTMENT nchar(20),
        MAJOR nchar(20),
        MAX int,
        PUNISHED int
    )
    CREATE TABLE administrator(
        AID char(15) PRIMARY KEY,
        PASSWORD char(70)
    )
    CREATE TABLE book(
        BID char(15) PRIMARY KEY,
        BNAME ntext,
        AUTHOR ntext,
        PUBLICATION_DATE char(17),
        PRESS nchar(20),
        POSITION char(10),
        SUM int,
        NUM int
    )
    CREATE TABLE borrowing_book(
        BID char(15),
        SID char(15),
        BORROW_DATE char(17),
        PUNISH int,
        PRIMARY KEY(BID, SID)
    )
    CREATE TABLE log(
        BID char(15),
        SID char(15),
        BORROW_DATE char(17),
        BACK_DATE char(17),
        PRIMARY KEY(BID, SID, BORROW_DATE)
    )
    ''')
    conn.commit()
    conn.close()


def main():
    with open('data/log', 'r+') as log:
        if(len(log.read()) == 0):
            init_database(CONFIG)
            print('empty')
        log.writelines(time.strftime("%Y-%m-%d %H:%M"))


if __name__ == '__main__':
    main()

import pymssql

CONFIG = {
    "host": '127.0.0.1:1433',
    "user": 'sa',
    "pwd": 'zyn121324',
    'db': 'test'
}


class MSSQL:
    def __init__(self, config: dict):
        self.__host = config['host']
        self.__user = config['user']
        self.__pwd = config['pwd']
        self.__db = config['db']
        self.conn = pymssql.connect(self.__host, self.__user, self.__pwd, self.__db)
        self.cursor = self.conn.cursor()
        if not self.cursor:
            raise(NameError, "connection failed")
            print('Error')

    def __del__(self):
        self.conn.close()

    def query(self, sql: str, val_list=None):
        self.cursor.execute(sql)
        ans = self.cursor.fetchall()
        for i in ans:
            print(i)


def main():
    try:
        temp = MSSQL(CONFIG)
        temp.query('''
            SELECT *
            FROM student
        ''')
    except NameError as e:
        print(e)


if __name__ == '__main__':
    main()
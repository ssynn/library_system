import pymssql

CONFIG = {
    "host": '127.0.0.1:1433',
    "user": 'sa',
    "pwd": '123456',
    'db': 'Library'
}


def main():
    # with open('data/log', 'r+') as log:
    #     if(len(log.read()) == 0):
    #         init_database(CONFIG)
    #         print('empty')
    #     log.writelines(time.strftime("%Y-%m-%d %H:%M"))
    # init_database(CONFIG)
    pass


if __name__ == '__main__':
    main()

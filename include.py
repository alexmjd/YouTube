import pymysql.cursors


# conn to db
def db_connect():
    return pymysql.connect(host='127.0.0.1',
                           user='root',
                           password='test',
                           db='mydb',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
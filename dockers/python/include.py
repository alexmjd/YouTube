import pymysql.cursors


# conn to db
def db_connect():
    return pymysql.connect(host='localhost',
                           user='user',
                           password='pass',
                           db='mydb',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
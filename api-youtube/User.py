from flask import Flask
import pymysql.cursors

app = Flask(__name__)
db_connect = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='test',
                             db='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def create_user(username, pseudo, email, password):
    return username


def get_users():
    try:
        with db_connect.cursor() as cursor:
            query = "select id, username, created_at, email from user"
            cursor.execute(query)
            result = {'Message ' : 'ok', 'data' : cursor.fetchall()}
    finally:
        db_connect.close()
        return result
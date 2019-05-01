import User
import pymysql.cursors
from flask import Flask
from flask_jsonpify import jsonify

db_connect = pymysql.connect(host='localhost',
                             user='root',
                             password='test',
                             db='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)


@app.route('/users')
def youtube():
    return jsonify(User.get_users())


@app.route('/')
def hello_world():
    return 'Hello World2'


if __name__ == '__main__':
    app.run()

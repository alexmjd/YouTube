import user
import pymysql.cursors
from flask import Flask
from flask_jsonpify import jsonify
from flask_restful import Resource, Api

db_connect = pymysql.connect(host='localhost',
                             user='root',
                             password='test',
                             db='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
api = Api(app)
# partie user
api.add_resource(user.User, '/users')
api.add_resource(user.UserById, '/user/<user_id>')


if __name__ == '__main__':
    app.run()

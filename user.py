from typing import Dict, Any, Union, Tuple

from flask import Flask
from flask_restful import Resource, Api
import pymysql.cursors
from flask_jsonpify import jsonify

app = Flask(__name__)
api = Api(app)
db_connect = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='test',
                             db='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


class User(Resource):
    def get(self):
        try:
            with db_connect.cursor() as users:
                query = "select id, username, created_at, email from user"
                users.execute(query)
                result = {'Message ': 'OK', 'data': users.fetchall(), 'pager': {'current': 'un chiffre', 'total': "cb"}}
        finally:
            return jsonify(result)


class UserById(Resource):
    def get(self, user_id):
        try:
            with db_connect.cursor() as cursor:
                query = "select id, username, created_at, email from user where id= %d" % int(user_id)
                cursor.execute(query)
                result = {'Message ': 'OK', 'data': cursor.fetchall()}
        finally:
            return jsonify(result)



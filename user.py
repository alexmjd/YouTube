from typing import Dict, Any, Union, Tuple
from flask import Flask, abort
from flask_restful import Resource, Api, http_status_message, reqparse, marshal
import pymysql.cursors
from flask_jsonpify import jsonify, request
from datetime import datetime

app = Flask(__name__)
api = Api(app)
db_connect = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='rootroot',
                             db='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def getIdByPseudo(pseudo):
    with db_connect.cursor() as cursor:
        query = "SELECT id FROM user WHERE pseudo= {}".format(pseudo)
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)
        return result


class GetUsers(Resource):
    def get(self):
        with db_connect.cursor() as users:
            query = "SELECT id, username, created_at, email from user"
            users.execute(query)
            result = {'Message ': 'OK', 'data': users.fetchall(), 'pager': {'current': 'un chiffre', 'total': "cb"}}
            return jsonify(result)


class CreateUser(Resource):
    def get_timestamp(self):
        return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, required=True, help='Username to create user')
            parser.add_argument('email', type=str, required=True, help='Email address to create user')
            parser.add_argument('pseudo', type=str, required=True, help='Pseudo to create user')
            parser.add_argument('password', type=str, required=True, help='Password to create user')
            args = parser.parse_args()

            _userUsername = args['username']
            _userEmail = args['email']
            _userPseudo = args['pseudo']
            _userPassword = args['password']
            with db_connect.cursor() as newUser:
                query = "INSERT INTO user (username, email, pseudo, password, created_at) VALUES ('{}', '{}', '{}', '{}', '{}')".format(_userUsername, _userEmail, _userPseudo, _userPassword, self.get_timestamp())
                newUser.execute(query)
                db_connect.commit()
                return {"Message": 'ok', 'data': '...'}, 201


class UserById(Resource):
    def get(self, user_id):
        with db_connect.cursor() as cursor:
            query = "SELECT id, username, created_at, email FROM user WHERE id= {}".format(user_id)
            if cursor.execute(query) == 1:
                return jsonify({'Message': 'OK', 'data': cursor.fetchall()})
            else:
                return abort(404, "not found")


    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required = True, help='Username to update user')
        parser.add_argument('email', type=str, required = True, help='Email address to update user')
        parser.add_argument('pseudo', type=str, required = True, help='Pseudo to update user')
        parser.add_argument('password', type=str, required = True, help='Password to update user')
        args = parser.parse_args()

        _userUsername = args['username']
        _userEmail = args['email']
        _userPseudo = args['pseudo']
        _userPassword = args['password']
        with db_connect.cursor() as newUser:
            query = "UPDATE user set username = '{}', email = '{}', pseudo = '{}', password = '{}' where id = '{}'".format(_userUsername, _userEmail, _userPseudo, _userPassword, user_id)
            if newUser.execute(query) == 1:
                db_connect.commit()
                return {"Message": 'OK', 'data': '...'}
            else:
                abort(404, "not found")


class DeleteUserById(Resource):
    def delete(self, user_id):
        with db_connect.cursor() as user:
            query = "DELETE from user where id = {}".format(user_id)
            if user.execute(query) == 1:
                db_connect.commit()
                return {}, 204
            else:
                abort(404, "not found")


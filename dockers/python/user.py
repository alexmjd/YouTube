from typing import Dict, Any, Union, Tuple
from flask import Flask
from flask_restful import Resource, Api, http_status_message, reqparse
import pymysql.cursors
from flask_jsonpify import jsonify, request
from datetime import datetime

app = Flask(__name__)
api = Api(app)
db_connect = pymysql.connect(host='t_db',
                             user='root',
                             password='root',
                             db='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


class GetUsers(Resource):
    def get(self):
        try:
            with db_connect.cursor() as users:
                query = "SELECT id, username, created_at, email from user"
                users.execute(query)
                result = {'Message ': 'OK', 'data': users.fetchall(), 'pager': {'current': 'un chiffre', 'total': "cb"}}
        finally:
            return jsonify(result)


class CreateUser(Resource):
    def get_timestamp(self):
        return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, help='Username to create user')
            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('pseudo', type=str, help='Pseudo to create user')
            parser.add_argument('password', type=str, help='Password to create user')
            args = parser.parse_args()

            _userUsername = args['username']
            _userEmail = args['email']
            _userPseudo = args['pseudo']
            _userPassword = args['password']

            with db_connect.cursor() as newUser:
                query = "INSERT INTO user (username, email, pseudo, password, created_at) VALUES ('%s', '%s', '%s', '%s', '%s')" % (_userUsername, _userEmail, _userPseudo, _userPassword, self.get_timestamp())
                newUser.execute(query)
                db_connect.commit()
                http_status_message(201)
                result = {"Message": 'ok', 'data': '...'}, 201
        except Exception as e:
            db_connect.rollback()
            return {'error': str(e)}
        finally:
            return jsonify(result)


class UserById(Resource):
    def get(self, user_id):
        try:
            with db_connect.cursor() as cursor:
                query = "SELECT id, username, created_at, email FROM user WHERE id= {}".format(user_id)
                cursor.execute(query)
                result = {'Message ': 'OK', 'data': cursor.fetchall()}
        finally:
            return jsonify(result)

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username to create user')
        parser.add_argument('email', type=str, help='Email address to create user')
        parser.add_argument('pseudo', type=str, help='Pseudo to create user')
        parser.add_argument('password', type=str, help='Password to create user')
        args = parser.parse_args()

        _userUsername = args['username']
        _userEmail = args['email']
        _userPseudo = args['pseudo']
        _userPassword = args['password']
        try:
            with db_connect.cursor() as newUser:
                query = "UPDATE user set username = '%s', email = '%s', pseudo = '%s', password = '%s' where id = '%s'" % (_userUsername, _userEmail, _userPseudo, _userPassword, user_id)
                newUser.execute(query)
                db_connect.commit()
                http_status_message(200)
                result = {"Message": 'OK', 'data': '...'}
        except Exception as e:
            db_connect.rollback()
            return {'error': str(e)}
        finally:
            return jsonify(result)


class DeleteUserById(Resource):
    def delete(self, user_id):
        try:
            with db_connect.cursor() as user:
                query = "DELETE from user where id = {}".format(user_id)
                user.execute(query)
                result = {'Message ': 'OK'}
        finally:
            return jsonify(result)


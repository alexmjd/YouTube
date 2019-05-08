import pymysql.cursors
import error
from flask import Flask, abort, make_response
from flask_restful import Resource,  reqparse
from flask_jsonpify import jsonify
from datetime import datetime

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
            query = "SELECT id, username, created_at, email, pseudo from user"
            users.execute(query)
            return make_response(jsonify({'Message ': 'OK', 'data': users.fetchall(), 'pager': {'current': 'un chiffre', 'total': "cb"}}))


class CreateUser(Resource):
    def get_timestamp(self):
        return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    def post(self):
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

            if _userUsername and _userEmail and _userPassword is not None:
                with db_connect.cursor() as newUser:
                    query = "INSERT INTO user (username, email, pseudo, password, created_at) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                        _userUsername, _userEmail, _userPseudo, _userPassword, self.get_timestamp())
                    newUser.execute(query)
                    db_connect.commit()
                    return make_response(UserById.get(self, str(newUser.lastrowid)), 201)
            else:
                return error.ifIsNone(10001, "Veuillez remplir tous les champs obligatoire!")




class UserById(Resource):
    def get(self, user_id):
        with db_connect.cursor() as cursor:
            id = error.ifIsInt(user_id)
            query = "SELECT id, username, created_at, email, pseudo FROM user WHERE id= {}".format(user_id)
            if id == len(user_id) and cursor.execute(query) == 1:
                return make_response(jsonify({'Message': 'OK', 'data': cursor.fetchone()}))
            else:
                return abort(404,  "Not found")

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username to update user')
        parser.add_argument('email', type=str, help='Email address to update user')
        parser.add_argument('pseudo', type=str, help='Pseudo to update user')
        parser.add_argument('password', type=str, help='Password to update user')
        args = parser.parse_args()

        _userUsername = args['username']
        _userEmail = args['email']
        _userPseudo = args['pseudo']
        _userPassword = args['password']

        if _userUsername and _userEmail and _userPassword and _userPassword is not None:
            with db_connect.cursor() as newUser:
                id = error.ifIsInt(user_id)
                query = "UPDATE user set username = '{}', email = '{}', pseudo = '{}', password = '{}' where id = '{}'".format(_userUsername, _userEmail, _userPseudo, _userPassword, user_id)
                if id == len(user_id) and newUser.execute(query) == 1:
                    db_connect.commit()
                    return self.get(user_id)
                else:
                    abort(404, "Not found")
        else:
            return error.ifIsNone(10001, "Veuillez à ne pas laisser les champs vides!")


class DeleteUserById(Resource):
    def delete(self, user_id):
        with db_connect.cursor() as user:
            id = error.ifIsInt(user_id) # if all of chars is int, return the same len than user id
            query = "DELETE from user where id = {}".format(user_id)
            if id == len(user_id) and user.execute(query) == 1:
                db_connect.commit()
                return {}, 204
            else:
                abort(404, "Not found")


class Authentification(Resource):
    def post(self):
        auth = reqparse.RequestParser()
        auth.add_argument('email', type=str, required=True, help="email")
        auth.add_argument('password', type=str, required=True, help="password")
        args = auth.parse_args()

        mail = args['email']
        passwd = args['password']
        with db_connect.cursor() as authenti:
            query = "SELECT id, username, created_at, email, pseudo FROM user WHERE email='{}' and password='{}'".format(mail, passwd)
            if authenti.execute(query) == 1:
                db_connect.commit()
                return make_response(jsonify({"Message": 'OK', 'token': authenti.fetchall()}), 201)
            else:
                abort(404, "Not found")


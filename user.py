from typing import Dict, Any, Union, Tuple
from flask import Flask
from flask_restful import Resource, Api
import pymysql.cursors
from flask_jsonpify import jsonify , request
from datetime import datetime
from flask_restful import http_status_message
app = Flask(__name__)
api = Api(app)
db_connect = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='test',
                             db='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


class GetUsers(Resource):
    def get(self):
        try:
            with db_connect.cursor() as users:
                query = "select id, username, created_at, email from user"
                users.execute(query)
                result = {'Message ': 'OK', 'data': users.fetchall(), 'pager': {'current': 'un chiffre', 'total': "cb"}}
        finally:
            return jsonify(result)


class CreateUser(Resource):
   def post(self):
       date = datetime.now()
       date_str = datetime.strftime(date, '%Y-%m-%d')
       try:
           with db_connect.cursor() as newUser:
               query = "insert into user (username, email, pseudo, password, created_at) values ('aryaStark', 'aryaS@yahoo.fr', 'AryaMastermind', 'teste98', '{}')" .format(date_str)
               newUser.execute(query)
               db_connect.commit()
               http_status_message(201)
               result = {"Message": 'OK', 'data': '...'}
       except Exception as e:
           db_connect.rollback()
           return {'error': str(e)}
       finally:
           return jsonify(result)


class UserById(Resource):
    def get(self, user_id):
        try:
            with db_connect.cursor() as cursor:
                query = "select id, username, created_at, email from user where id= {}".format(user_id)
                cursor.execute(query)
                result = {'Message ': 'OK', 'data': cursor.fetchall()}
        finally:
            return jsonify(result)


    def put(self, user_id):
        name = "dy"
        mail = "modif@gmail.com"
        psdo = "psyyy"
        passwd = "190998"
        try:
            with db_connect.cursor() as newUser:
                query = "update user set username = {}, email = {}, pseudo = {}, password = {} where id = {}".format(name, mail, psdo, passwd, user_id)
                newUser.execute(query)
                db_connect.commit()
                http_status_message(201)
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
                query = "delete from user where id = {}".format(user_id)
                user.execute(query)
                result = {'Message ': 'OK'}
        finally:
            return jsonify(result)
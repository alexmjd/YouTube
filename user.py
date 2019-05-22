import logging
from flask_httpauth import HTTPBasicAuth
from flask import make_response
from flask_restful import Resource, reqparse
from flask_jsonpify import jsonify
from datetime import datetime
from app import db, ma
from SchemaSQLA import UserSchema, User


auth = HTTPBasicAuth()
directly_id = 0
# init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

import include
import error
db_connect = include.db_connect()


def get_id_user():
    return directly_id


class GetUsers(Resource):
        def get(self):
            parser = reqparse.RequestParser()
            parser.add_argument('pseudo', type=str)
            parser.add_argument('page', type=str)
            parser.add_argument('perPage', type=str)
            args = parser.parse_args()

            _userPseudo = args['pseudo'] if args['pseudo'] else ''
            _page = int(args['page']) if args['page'] and args['page'] is not "0" and args['page'].isdigit() else 1
            _perPage = int(args['perPage']) if args['perPage'] and args['perPage'] is not "0" and args['perPage'].isdigit() else 50

            start_index = _perPage * _page - _perPage

            all_users = User.query.all()
            result = users_schema.dump(all_users)
            result = result.data[start_index:start_index+_perPage]
            return make_response(jsonify({'Message ': 'OK', 'data': result, 'pager': {'current': _page, 'total': len(result)}}))


class CreateUser(Resource):
    def get_timestamp(self):
        return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    def post(self):
        if get_id_user() != 0:
            return jsonify({"Message" : "Mec t'es déjà co"})
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
        stack = str(error.tchek_username(_userUsername)) + str(error.tchek_email(_userEmail)) + str(
            error.tchek_password(_userPassword))
        logging.info("We are here, create user \n")
        if _userUsername and _userEmail and _userPassword is not None:
            if stack != "":
                logging.info(stack)
                return error.badRequest(10034, stack)
            new_user = User(_userUsername, _userEmail, _userPseudo, _userPassword)
            db.session.add(new_user)
            db.session.commit()
            result = user_schema.dump(new_user).data
            return make_response(jsonify({'Message': 'OK', 'data': result}), 201)
        else:
            return error.badRequest(10001, "Veuillez remplir tous les champs obligatoire!")


class UserById(Resource):
    def get(self, user_id):
        if error.ifId(user_id) is False:
            return error.notFound()
        token_head = include.header()
        if error.ifToken(user_id, token_head) is True:
            getUser = User.query.get(user_id)
            data = UserSchema().dump(getUser).data
        else:
            data = include.get_user_by_id(user_id)
        if data != False:
            return make_response(jsonify({'Message': 'OK', 'data': data}))
        else:
            return error.badRequest(10005, "erreur dans le traitement de la requête")

    def put(self, user_id):
        if error.ifId(user_id) is False:
            return error.notFound()
        token_head = include.header()
        user_id_token = str(include.get_user_id_by_token(token_head))
        if error.ifToken(directly_id, token_head) is True and token_head is not None:
            if user_id_token != user_id:
                return error.forbidden()
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
            stack = str(error.tchek_username(_userUsername)) + str(error.tchek_email(_userEmail)) + str(
                error.tchek_password(_userPassword))
            if _userPseudo is None:
                _userPseudo = ""

            if _userUsername and _userEmail and _userPassword and _userPassword is not None:
                if stack != "":
                    return error.badRequest(10034, stack)
                user = User.query.get(user_id)
                if user is not None:
                    user.username = _userUsername
                    user.email = _userEmail
                    user.pseudo = _userPseudo
                    user.password = _userPassword
                    db.session.commit()
                    return self.get(user_id)
                else:
                    return error.badRequest(10005, "erreur dans le traitement de la requête")
            else:
                return error.badRequest(10001, "Veuillez remplir tous les champs obligatoire!")
        else:
            return error.unauthorized()

    def delete(self, user_id):
        if error.ifId(user_id) is False:
            return error.notFound()
        token_head = include.header()
        user_id_token = str(include.get_user_id_by_token(token_head))
        if error.ifToken(directly_id, token_head) is True and token_head is not None:
            if user_id_token != user_id:
                return error.forbidden()
            include.delete_token(user_id)
            user = User.query.get(user_id)
            if user is not None:
                db.session.delete(user)
                db.session.commit()
                return {}, 204
            else:
                return error.badRequest(10005, "erreur dans le traitement de la requête")
        else:
            return error.unauthorized()


class Authentification(Resource):
    def post(self):
        global directly_id
        auth = reqparse.RequestParser()
        auth.add_argument('username', type=str, required=True)
        auth.add_argument('password', type=str, required=True)
        args = auth.parse_args()

        usern = args['username']
        passwd = args['password']
        directly_id = str(include.authen(usern, passwd))
        if directly_id != "0" and (error.ifToken(directly_id, None) == False or error.tchek_token_expiration(directly_id) == True):
            user_token = include.create_token()
            include.add_token(user_token, directly_id)
        else:
            user_token = include.get_token_by_user(directly_id)
        data = include.get_user_by_id(directly_id)
        if data != False:
            return make_response(jsonify({"Message": 'OK', 'data': {'token': user_token, 'user': data}}), 201)
        else:
            return error.badRequest(10002, "Identifiant ou mot de passe invalide !")

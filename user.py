import include
import error
#import app
from app import db, ma
from flask import abort, make_response
from flask_restful import Resource,  reqparse
from flask_jsonpify import jsonify
from datetime import datetime
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required
                                , jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


db_connect = include.db_connect()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pseudo = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, pseudo, password):
        self.username = username
        self.email = email
        self.pseudo = pseudo
        self.password = password
        self.created_at = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'username', 'email', 'pseudo', 'created_at')


# init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

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

            limit = _perPage * _page - _perPage

            # with db_connect.cursor() as users:
            #     query = "SELECT id, username, created_at, email, pseudo from user WHERE pseudo LIKE '%{}%' ORDER BY pseudo LIMIT {}, {}".format(_userPseudo, limit, _perPage)
            #     users.execute(query)
            all_users = User.query.all()
            result = users_schema.dump(all_users)
            print(len(result.data))
            return make_response(jsonify({'Message ': 'OK', 'data': result.data, 'pager': {'current': _page, 'total': len(result.data)}}))


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
                new_user = User(_userUsername, _userEmail, _userPseudo, _userPassword)
                db.session.add(new_user)
                db.session.commit()

                result = user_schema.dump(new_user).data
                return make_response(jsonify({'Message': 'OK', 'data': result}), 201)
            else:
                return error.ifIsNone(10001, "Veuillez remplir tous les champs obligatoire!")


class UserById(Resource):
    def get(self, user_id):
        id = error.ifIsInt(user_id)

        if id == len(user_id):
            user = User.query.get(user_id)
            result = user_schema.dump(user).data
            return make_response(jsonify({'Message': 'OK', 'data': result}))
        else:
            return abort(404,  "Not found")

    def put(self, user_id):
        id = error.ifIsInt(user_id)

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
            if id == len(user_id):
                user = User.query.get(user_id)

                user.email = _userUsername
                user.username = _userEmail
                user.pseudo = _userPseudo
                user.password = _userPassword

                db.session.commit()
                return self.get(user_id)
            else:
                abort(404, "Not found")
        else:
            return error.ifIsNone(10001, "Veuillez à ne pas laisser les champs vides!")

    def delete(self, user_id):
        #with db_connect.cursor() as user:
        id = error.ifIsInt(user_id) # if all of chars is int, return the same len than user id
        #    query = "DELETE from user where id = {}".format(user_id)
        if id == len(user_id):
            user = User.query.get(user_id)
            db.session.delete(user)
            db.session.commit()
            return {}, 204
        else:
            abort(404, "Not found")


class Authentification(Resource):
    def post(self):
        auth = reqparse.RequestParser()
        auth.add_argument('username', type=str, required=True, help="user")
        auth.add_argument('password', type=str, required=True, help="password")
        args = auth.parse_args()

        user = args['username']
        passwd = args['password']
        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        with db_connect.cursor() as authenti:
            query = "SELECT id, username, created_at, email, pseudo FROM user WHERE username ='{}' and password='{}'".format(
                user, passwd)
            if authenti.execute(query) == 1:
                db_connect.commit()
                return make_response(
                    jsonify({"Message": 'OK', 'identity': get_jwt_identity(), 'data': {'token': access_token, 'user': authenti.fetchall()}}), 201)
            else:
                return error.ifIsNone(10001, "identifiant ou mot de passe invalide!")

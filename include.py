import pymysql.cursors
import user
import secrets
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required
                                , jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask_restful import reqparse
from user import UserSchema, User
from SchemaSQLA import Token, TokenSchema, User, UserSchema
from app import db, ma
# conn to db
def db_connect():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='rootroot',
                           db='mydb',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


jwt_token = ""
import error

######################## get #############################################
def get_username_by_id(user_id):
    name = User.query.get(user_id)
    if name is not None:
        data = UserSchema().dump(name).data
        return data['username']
    else:
        return error.badRequest(10001, "Impossible de récupérer l'username !")


def get_user_by_id(user_id):
    userbyid = User.query.get(user_id)
    if userbyid is None:
        return False
    data = UserSchema().dump(userbyid).data
    if user.get_id_user() == user_id:
        return data
    else:
        return {'id':data['id'], 'username':data['username'], 'pseudo':data['pseudo'], 'created_at':data['created_at']}


def get_user_id_by_token(token):
    userId = Token.query.filter_by(code=token).first()
    if userId is not None:
        data = TokenSchema().dump(userId).data
        return data['user_id']
    else:
        return False


def get_token_by_user(id_user):
    tok = Token.query.filter_by(user_id=id_user).first()
    if tok is not None:
        data = TokenSchema().dump(tok).data
        return data['code']
    else:
        return False


"""
    Authentification
"""
def authen(usern, passwd):
    auth = User.query.filter_by(username=usern, password=passwd).first()
    if auth is not None:
        data = UserSchema().dump(auth).data
        return data['id']
    else:
        return 0


""" 
    TOKEN
"""
def add_token(token, id_user):
    new_token = Token(token, id_user)
    db.session.add(new_token)
    db.session.commit()


def delete_token(id_user):
    tok = Token.query.filter_by(user_id=id_user).first()
    db.session.delete(tok)
    db.session.commit()


def create_token():
    user_token = secrets.token_urlsafe()
    return user_token


"""
    JWT
"""
def create_JWT(username):
    jwt_access_token = create_access_token(identity=username)
    jwt_refresh_token = create_refresh_token(identity=username)
    global jwt_token
    jwt_token = jwt_access_token


def get_jwt():
    global jwt_token
    return jwt_token

"""
    HEADER
"""

#prend le token dans le header
def header():
    header = reqparse.RequestParser()
    header.add_argument('token', type=str, location="headers", help="unauthorized")
    head = header.parse_args()
    if head['token'] == '':
        head['token'] = None
    return head['token']
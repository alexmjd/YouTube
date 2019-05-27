from flask import make_response
from flask_jsonpify import jsonify
from datetime import datetime, timedelta
import re
import include, logging
from SchemaSQLA import Token, TokenSchema, User, UserSchema, Video, VideoSchema

dab = include.db_connect()

"""
    Return number of ints in user_id
"""


def ifId_video(id_video):
    vid = Video.query.get(id_video)
    if vid is not None:
        data = VideoSchema().dump(vid).data
        return data['id']
    else:
        return False


def user_id_by_video_id(video_id):
    vid = Video.query.get(video_id)
    if vid is not None:
        data = VideoSchema().dump(vid).data
        return str(data['user_id'])
    else:
        return -1
    #with dab.cursor() as cursor:
    #    query = "SELECT id FROM video where id = {}".format(id_video)
    #    if cursor.execute(query) == 1:
    #        data = cursor.fetchone()
    #        return data['id']
    #    else:
    #        return False


def badRequest(code, message_data):
    return make_response(jsonify({"Message": "Bad Request", "code": code, "data": [message_data]}), 400)


def unauthorized():
    return make_response(jsonify({"Message": "Unauthorized"}), 401)


def notFound():
    return make_response(jsonify({"Message": "Not found"}), 404)


def forbidden():
    return make_response(jsonify({"Message": "Forbidden"}), 403)


def tchek_password(passwd):
    if len(passwd) < 8:
        return " Mot de passe trop court, "
    else:
        return ""


def ifId(id_user):
    id = User.query.get(id_user)
    if id is not None:
        result = UserSchema().dump(id).data
        return result['id']
    else:
        return False


def tchek_username(user):
    usern = User.query.filter_by(username=user).first()
    if usern is not None:
        return "Cette username est déjà utilisé, "
    else:
        return ""


def tchek_email(mail):
    match = re.match('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', mail)
    if match == None:
        return 'Mail invalide, '
    Email = User.query.filter_by(email=mail).first()
    if Email is not None:
        return "Cette email est déjà utilisée, "
    else:
        return ""


def ifToken(id_user, token_data):
    token = False
    tok = Token.query.filter_by(user_id=id_user).first()
    if tok is not None:
        if token_data is None:
            return True
        data = TokenSchema().dump(tok).data
        if data['code'] == token_data:
            token = True
    return token


def tchek_token_expiration(id_user):
    expir = Token.query.filter_by(user_id=id_user).first()
    if expir is not None:
        data = TokenSchema().dump(expir).data
        if data['expired_at'] < datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
            include.delete_token(id_user)
            return True
        else:
            return False
    else:
        return True
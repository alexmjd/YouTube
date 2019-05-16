from flask import make_response
from flask_jsonpify import jsonify
import user, include
from datetime import datetime, timedelta

db = include.db_connect()

"""
Return number of ints in user_id
"""
def ifIsInt(user_id):
    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    car = 0
    for n in range(0, len(nums)):
        for i in range(0, len(user_id)):
            if user_id[i] == nums[n]:
                car = car + 1
    return car


def ifIsNone(code, message_data):
    return make_response(jsonify({"Message": "Bad Request", "code": code, "data": [message_data]}), 400)

def unauthorized():
    return make_response(jsonify({"Message": "Unauthorized"}), 401)


def tchek_token_expiration(id_user):
    with db.cursor() as cursor:
        query = "SELECT expired_at FROM token where user_id = {}".format(id_user)
        if cursor.execute(query) == 1:
            data = cursor.fetchone()
            expired_at = data['expired_at']
            if expired_at < datetime.now():
                include.delete_token(id_user)
                return True
            else:
                return False
        else:
            return True


def ifToken(id_user):
    with db.cursor() as cursor:
        query = "SELECT user_id FROM token where user_id = {}".format(id_user)
        if cursor.execute(query) == 1:
            return True
        else:
            return False
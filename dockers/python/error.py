from flask import make_response
from flask_jsonpify import jsonify
import user, include

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
from flask import Flask, make_response
from flask_restful import Resource, Api, http_status_message, reqparse, marshal
import pymysql.cursors
from urllib.parse import urlparse
from flask import render_template

from flask_jsonpify import jsonify, request
from datetime import datetime

app = Flask(__name__)
api = Api(app)
db_connect = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='test',
                             db='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def ifInt(user_id):
    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    car = 0
    for n in range(0, len(nums)):
        for i in range(0, len(user_id)):
            if user_id[i] == nums[n]:
                car = car + 1
    return car


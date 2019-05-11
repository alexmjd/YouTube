import include
from flask import make_response
from flask_restful import Resource
from flask_jsonpify import jsonify

db_connect = include.db_connect()

class GetVideos(Resource):
    def get(self):
        list = []
        with db_connect.cursor() as video:
            query = "SELECT * FROM video"
            video.execute(query)
            results = video.fetchall()
            return make_response(jsonify({'Message ': 'OK', 'data': results, 'pager': {'current': 1, 'total': video.rowcount}}))

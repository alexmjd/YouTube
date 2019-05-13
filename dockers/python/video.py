import include
import error
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

class GetVideoById(Resource):
    def get(self, video_id):
        with db_connect.cursor() as video:
            id = error.ifIsInt(video_id)
            query = "SELECT * FROM video WHERE id = {}".format(video_id)
            if id == len(video_id) and video.execute(query) == 1:
                return make_response(jsonify({'Message': 'OK', 'data': video.fetchone()}))
            else:
                return abort(404,  "Not found")
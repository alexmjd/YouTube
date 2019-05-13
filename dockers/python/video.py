import include
import error
from flask import abort, make_response
from flask_restful import Resource, reqparse
from datetime import datetime
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

class CreateVideo(Resource):
    def get_timestamp(self):
        return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    def post(self, user_id):
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='name of the video')
            parser.add_argument('source', type=str, help='file of the video')
            args = parser.parse_args()

            _name = args['name']
            _source = args['source']

            if _name and _source is not None:
                with db_connect.cursor() as video:
                    id = error.ifIsInt(user_id)
                    query = "INSERT INTO video (name, duration, user_id, source, created_at, view, enabled) VALUES ('{}', 300, 2, '{}', '{}', 0, 1)".format(
                        _name,
                        _source,
                        self.get_timestamp())
                    if id == len(user_id) and video.execute(query) == 1:
                        db_connect.commit()
                        return make_response(GetVideoById.get(self, str(video.lastrowid)), 201)
                    else:
                        abort(404, "Not allowed")
            else:
                return error.ifIsNone(10001, "Veuillez remplir tous les champs obligatoire!")

class GetVideoById(Resource):
    def get(self, video_id):
        with db_connect.cursor() as video:
            id = error.ifIsInt(video_id)
            query = "SELECT * FROM video WHERE id = {}".format(video_id)
            if id == len(video_id) and video.execute(query) == 1:
                return make_response(jsonify({'Message': 'OK', 'data': video.fetchone()}))
            else:
                return abort(404,  "Not found")

    def put(self, video_id):
        with db_connect.cursor() as video:
            return 0

    def delete(self, video_id):
        with db_connect.cursor() as video:
            id = error.ifIsInt(video_id)
            query = "DELETE FROM video WHERE id = {}".format(video_id)
            if id == len(video_id) and video.execute(query) == 1:
                db_connect.commit()
                return {}, 204
            else:
                abort(404, "Not found")

class GetVideosByIdUser(Resource):
    def get(self, user_id):
        with db_connect.cursor() as videos:
            id = error.ifIsInt(user_id)
            query = "SELECT * FROM video WHERE user_id = {}".format(user_id)
            if id == len(user_id) and videos.execute(query) > 0:
                return make_response(jsonify({'Message': 'OK', 'data': videos.fetchall()}))
            else:
                abort(404, "Not found")
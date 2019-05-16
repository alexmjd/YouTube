import include, error, upload, logging, user
from flask import abort, make_response
from flask_restful import Resource, reqparse
from datetime import datetime
from flask_jsonpify import jsonify

db_connect = include.db_connect()


class GetVideos(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('page', type=str)
        parser.add_argument('perPage', type=str)
        args = parser.parse_args()

        _name = args['name'] if args['name'] else ''
        _page = int(args['page']) if args['page'] and args['page'] is not "0" and args['page'].isdigit() else 1
        _perPage = int(args['perPage']) if args['perPage'] and args['perPage'] is not "0" and args['perPage'].isdigit() else 50

        limit = _perPage * _page - _perPage

        with db_connect.cursor() as video:
            query = "SELECT * FROM video LIMIT {}, {}".format(limit, _perPage)
            video.execute(query)
            results = video.fetchall()
            return make_response(jsonify({'Message ': 'OK', 'data': results, 'pager': {'current': _page, 'total': video.rowcount}}))

class CreateVideo(Resource):
    def get_timestamp(self):
        return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    def post(self, user_id):
        if error.ifToken(user.get_id_user()) is True:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='name of the video')
            parser.add_argument('source', type=str, help='file of the video')
            args = parser.parse_args()

            uploader = upload.Upload()

            _name = args['name']
            _source = uploader.upload_file()

            logging.warning(_source)
            #_source = args['source']

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
        else:
            return error.unauthorized()


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
        if error.ifToken(user.get_id_user()) is True:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='Name of the video')
            parser.add_argument('user_id', type=int, help='Id of the user')
            args = parser.parse_args()

            _name = args['name']
            _user_id = args['user_id']

            if _name and _user_id is not None:
                with db_connect.cursor() as video:
                    id = error.ifIsInt(video_id)
                    query = "UPDATE video SET name = '{}', user_id = {} WHERE id = {}".format(_name, _user_id, video_id)
                    if id == len(video_id) and video.execute(query) == 1:
                        db_connect.commit()
                        return self.get(video_id)
                    else:
                        abort(404, "Not found")
            else :
                return error.ifIsNone(10001, "Inputs are missed")
        else:
            return error.unauthorized()

    def delete(self, video_id):
        if error.ifToken(user.get_id_user()) is True:
            with db_connect.cursor() as video:
                id = error.ifIsInt(video_id)
                query = "DELETE FROM video WHERE id = {}".format(video_id)
                if id == len(video_id) and video.execute(query) == 1:
                    db_connect.commit()
                    return {}, 204
                else:
                    abort(404, "Not found")
        else:
            return error.unauthorized()

    def patch(self, video_id):
        
        # En attendant le JWT, on fait avec le token simple
        if error.ifToken(user.get_id_user()) is False:
            
            parser = reqparse.RequestParser()
            parser.add_argument('format', type=str, help='Name of the video')
            args = parser.parse_args()

            formatVideo = args['format'] if args['format'] else '480'

            with db_connect.cursor() as video:
                id = error.ifIsInt(video_id)
                query = "INSERT INTO video_format(code, uri, video_id) VALUES ({}, 'uri de test', {})".format(formatVideo, video_id)

                if id == len(video_id) and video.execute(query) == 1:
                    #video.execute(query)
                    retourVid = GetVideoById.get(self, video_id)
                    return make_response(retourVid)
                    return make_response(jsonify({'message':'OK', 'data':retourVid}))
                else:
                    return make_response(jsonify({'message':"no"}))
        else :
            return make_response(jsonify({'message':'no token'}))



class GetVideosByIdUser(Resource):
    def get(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=str)
        parser.add_argument('perPage', type=str)
        args = parser.parse_args()

        _page = int(args['page']) if args['page'] and args['page'] is not "0" and args['page'].isdigit() else 1
        _perPage = int(args['perPage']) if args['perPage'] and args['perPage'] is not "0" and args['perPage'].isdigit() else 50

        limit = _perPage * _page - _perPage

        with db_connect.cursor() as videos:
            id = error.ifIsInt(user_id)
            query = "SELECT * FROM video WHERE user_id = {} LIMIT {}, {}".format(user_id, limit, _perPage)
            if id == len(user_id) and videos.execute(query) > 0:
                return make_response(jsonify({'Message': 'OK', 'data': videos.fetchall(), 'pager': {'current': _page, 'total': videos.rowcount}}))

            else:
                abort(404, "Not found")
import include, error, user
from flask import abort, make_response
from flask_restful import Resource, reqparse
from flask_jsonpify import jsonify

db_connect = include.db_connect()

directly_id = user.get_id_user()


class GetComments(Resource):
        def get(self, video_id):
            parser = reqparse.RequestParser()
            parser.add_argument('pseudo', type=str)
            parser.add_argument('page', type=str)
            parser.add_argument('perPage', type=str)
            args = parser.parse_args()

            _userPseudo = args['pseudo'] if args['pseudo'] else ''
            _page = int(args['page']) if args['page'] and args['page'] is not "0" and args['page'].isdigit() else 1
            _perPage = int(args['perPage']) if args['perPage'] and args['perPage'] is not "0" and args['perPage'].isdigit() else 50

            limit = _perPage * _page - _perPage

            list = []
            with db_connect.cursor() as comments:
                query = "SELECT id, body, user_id FROM comment WHERE video_id='{}' LIMIT {}, {}".format(video_id, limit, _perPage)
                comments.execute(query)
                result = comments.fetchall()
                for row in result:
                    listTmp = {
                        'id': row['id'],
                        'body': row['body'],
                        'user': UserById.get(self, row['user_id'])
                    }
                    list.append(listTmp)
                return make_response(jsonify({'Message ': 'OK', 'data': list, 'pager': {'current': _page, 'total': comments.rowcount}}))


class CreateComments(Resource):
    def post(self, video_id):
        if error.ifToken(user.get_id_user()) is True:
            parser = reqparse.RequestParser()
            parser.add_argument('body', type=str, help='Body to create comment')
            args = parser.parse_args()

            _commentBody = args['body']

            _userId = user.get_id_user()
            if _commentBody is not None:
                with db_connect.cursor() as newComment:
                    query = "INSERT INTO comment (body, user_id, video_id) VALUES ('{}', '{}', '{}')".format(
                        _commentBody, _userId, video_id)
                    newComment.execute(query)
                    db_connect.commit()
                    row = newComment.fetchone()
                    return make_response(CommentById.get(self, str(newComment.lastrowid)), 201)
            else:
                return error.ifIsNone(10001, "Veuillez remplir tous les champs obligatoire!")
        else:
            error.unauthorized()


class CommentById(Resource):
    def get(self, comment_id):
        with db_connect.cursor() as cursor:
            id = error.ifIsInt(comment_id)
            query = "SELECT id, body, user_id FROM comment WHERE id= {}".format(comment_id)
            if id == len(comment_id) and cursor.execute(query) == 1:
                row = cursor.fetchone()
                return make_response(jsonify({'Message': 'OK', 'data': row, 'user': UserById.get(self, row['user_id'])}))
            else:
                return abort(404,  "Not found")


class UserById:
    def get(self, user_id):
        with db_connect.cursor() as cursor:
            query = "SELECT id, username, created_at, email, pseudo FROM user WHERE id= {}".format(user_id)
            if cursor.execute(query) == 1:
                return cursor.fetchone()
            else:
                return "Not found"

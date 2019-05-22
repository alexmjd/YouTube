import include, error, user
from flask import abort, make_response
from flask_restful import Resource, reqparse
from flask_jsonpify import jsonify
from app import db, ma
from SchemaSQLA import Comment, CommentSchema, User, UserSchema

db_connect = include.db_connect()


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
        com = Comment.query.filter_by(video_id=video_id).first()
        if com is not None:
            data = CommentSchema().dump(com).data
            for row in data:
                listTmp = {
                    'id': row['id'],
                    'body': row['body'],
                    'user': UserById.get(self, row['user_id'])
                }
                list.append(listTmp)
            return make_response(jsonify({'Message ': 'OK', 'data': list, 'pager': {'current': _page, 'total': data.rowcount}}))
        else:
            return error.badRequest(10005)
        #with db_connect.cursor() as comments:
        #    query = "SELECT id, body, user_id FROM comment WHERE video_id='{}' LIMIT {}, {}".format(video_id, limit, _perPage)
        #    comments.execute(query)
        #    result = comments.fetchall()

         #   return make_response(jsonify({'Message ': 'OK', 'data': list, 'pager': {'current': _page, 'total': comments.rowcount}}))


class CreateComments(Resource):
    def post(self, video_id):
        if error.ifId_video(video_id) is False:
            return error.notFound()
        token_head = include.header()
        directly_id = user.get_id_user()
        if error.ifToken(directly_id, token_head) is True and token_head is not None:
            parser = reqparse.RequestParser()
            parser.add_argument('body', type=str, help='Body to create comment')
            args = parser.parse_args()

            _commentBody = args['body']

            _userId = user.get_id_user()
            if _commentBody is not None and _commentBody is not "":
                new_comment = Comment(_commentBody, _userId, video_id)
                db.session.add(new_comment)
                db.session.commit()
                result = CommentSchema().dump(new_comment).data
                #with db_connect.cursor() as newComment:
                #    query = "INSERT INTO comment (body, user_id, video_id) VALUES ('{}', '{}', '{}')".format(
                #        _commentBody, _userId, video_id)
                #    newComment.execute(query)
                #    db_connect.commit()
                #    row = newComment.fetchone()
                return make_response(CommentById.get(self, str(result['id'])), 201)
            else:
                return error.badRequest(10001, "Veuillez remplir tous les champs obligatoire!")
        else:
           return error.unauthorized()


class CommentById(Resource):
    def get(self, comment_id):
        if error.ifId(comment_id) == False:
            return error.notFound()
        com = Comment.query.get(comment_id)
        if com is not None:
            data = CommentSchema().dump(com).data
            return make_response(jsonify({'Message': 'OK', 'data': data, 'user': UserById.get(self, data['user_id'])}))
        else:
            return error.notFound()


class UserById:
    def get(self, user_id):
        user = User.query.get(user_id)
        if user is not None:
            data = UserSchema().dump(user).data
            return data
        else:
            return error.notFound()

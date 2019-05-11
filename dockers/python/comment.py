import include
from flask import make_response
from flask_restful import Resource
from flask_jsonpify import jsonify

db_connect = include.db_connect()


class GetComments(Resource):
        def get(self, video_id):
            list = []
            with db_connect.cursor() as comments:
                query = "SELECT id, body, user_id FROM comment WHERE video_id='{}'".format(video_id)
                comments.execute(query)
                result = comments.fetchall()
                for row in result:
                    listTmp = {
                        'id': row['id'],
                        'body': row['body'],
                        'user': UserById.get(self, row['user_id'])
                    }
                    list.append(listTmp)
                return make_response(jsonify({'Message ': 'OK', 'data': list, 'pager': {'current': '1', 'total': comments.rowcount}}))


class UserById:
    def get(self, user_id):
        with db_connect.cursor() as cursor:
            query = "SELECT id, username, created_at, email, pseudo FROM user WHERE id= {}".format(user_id)
            if cursor.execute(query) == 1:
                return cursor.fetchone()
            else:
                return "Not found"

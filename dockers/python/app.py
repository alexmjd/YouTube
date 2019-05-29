import logging
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from models.users import user as user
from models.comment import comment as comment
from models.video import video
from models.auth import auth as auth
import config

logging.getLogger().setLevel(logging.INFO)

app = config.app

api = Api(app)
CORS(app)

# Create a URL route in our application for "/"
@app.route('/')
def home():
    return 'home route'


# partie user
api.add_resource(user.Users, '/users', methods=['GET'])
api.add_resource(user.User, '/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
api.add_resource(user.UserById, '/user', methods=['POST'])

api.add_resource(auth.Authentification, '/auth', methods=['POST'])

api.add_resource(comment.Comments, '/video/<video_id>/comments', methods=['GET'])
api.add_resource(comment.CreateComments, '/video/<video_id>/comment', methods=['POST'])
api.add_resource(comment.CommentById, '/comment/<comment_id>', methods=['GET'])

api.add_resource(video.Videos, '/videos', methods=['GET'])
api.add_resource(video.Video, '/video/<video_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
api.add_resource(video.VideosByUser, '/user/<user_id>/videos', methods=['GET'])
api.add_resource(video.VideoByUser, '/user/<user_id>/video', methods=['POST'])


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
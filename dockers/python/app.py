import user
import comment
import upload
import video
import os
import logging
from flask import Flask, flash, request, redirect, url_for, make_response, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
from flask_jsonpify import jsonify
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)
api = Api(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': 'Not found'}), 404)

#erreur 401 JWT
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return make_response(jsonify({'Message': 'Unauthorized'}), 401)


# partie user
api.add_resource(user.GetUsers, '/users')
api.add_resource(user.UserById, '/user/<user_id>')
api.add_resource(user.CreateUser, '/user')
api.add_resource(user.Authentification, '/auth')

# Partie commentaires
api.add_resource(comment.GetComments, '/video/<video_id>/comments')
api.add_resource(comment.CreateComments, '/video/<video_id>/comment')

# Partie vidéo
api.add_resource(video.GetVideos, '/videos')
api.add_resource(video.GetVideoById, '/video/<video_id>')
api.add_resource(video.GetVideosByIdUser, '/user/<user_id>/videos')
api.add_resource(video.CreateVideo, '/user/<user_id>/video', methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

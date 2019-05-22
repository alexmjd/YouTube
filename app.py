import logging
from flask import Flask, make_response, jsonify
from flask_jwt_extended import JWTManager
from flask_jsonpify import jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootroot@localhost/mydb'
# db init
db = SQLAlchemy(app)
# ma init
ma = Marshmallow(app)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)
api = Api(app)


import user, comment, upload, video
logging.getLogger().setLevel(logging.INFO)


@app.errorhandler(500)
def inattendu(error):
    return  make_response(jsonify({'message': 'Une erreur inattendu est survenu'}), 500)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': 'Not found'}), 404)


#erreur 401 JWT
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return make_response(jsonify({'Message': 'Unauthorized'}), 401)


@app.before_first_request
def create_tables():
    db.create_all()


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

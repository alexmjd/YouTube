from flask import Flask, make_response, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from sqlalchemy import create_engine, and_, text
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
api = Api(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootroot@localhost/mydb'
# db init
db = SQLAlchemy(app)
# ma init
ma = Marshmallow(app)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

import user, comment

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': 'Not found'}), 404)


@app.before_first_request
def create_tables():
    db.create_all()


# partie user
api.add_resource(user.GetUsers, '/users')
api.add_resource(user.UserById, '/user/<user_id>')
api.add_resource(user.CreateUser, '/user')
api.add_resource(user.Authentification, '/auth')
# partie comment
api.add_resource(comment.GetComments, '/video/<video_id>/comments')
api.add_resource(comment.CreateComments, '/video/<video_id>/comment')


if __name__ == '__main__':
    app.run()

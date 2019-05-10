import user
from flask import Flask, make_response, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)
api = Api(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': 'Not found'}), 404)


# partie user
api.add_resource(user.GetUsers, '/users')
api.add_resource(user.UserById, '/user/<user_id>')
api.add_resource(user.CreateUser, '/user')
api.add_resource(user.Authentification, '/auth')


if __name__ == '__main__':
        app.run(host="0.0.0.0", port=5000)
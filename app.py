import user
from flask import Flask, make_response, jsonify
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
# partie user
api.add_resource(user.GetUsers, '/users')
api.add_resource(user.DeleteUserById, '/users/<user_id>')
api.add_resource(user.UserById, '/user/<user_id>')
api.add_resource(user.CreateUser, '/user')
api.add_resource(user.Authentification, '/auth')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': 'Not found'}), 404)


if __name__ == '__main__':
    app.run()

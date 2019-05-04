import user
import error
from flask import render_template
from flask import abort
from flask import Flask, make_response, jsonify
from flask_restful import Api, http_status_message

app = Flask(__name__)
api = Api(app)
# partie user
api.add_resource(user.GetUsers, '/users')
api.add_resource(user.DeleteUserById, '/users/<user_id>')
api.add_resource(user.UserById, '/user/<user_id>')
api.add_resource(user.CreateUser, '/user')


if __name__ == '__main__':
    app.run()

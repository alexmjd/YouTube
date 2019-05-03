import user
import pymysql.cursors
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
# partie user
api.add_resource(user.GetUsers, '/users')
api.add_resource(user.DeleteUserById, '/users/<user_id>')
api.add_resource(user.UserById, '/user/<user_id>')
api.add_resource(user.CreateUser, '/user')


if __name__ == '__main__':
    app.run()

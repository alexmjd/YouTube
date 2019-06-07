from flask import Flask
from flask_restful import Resource, Api
import config

app = config.app

@app.route('/')
def home():
    return "pong"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
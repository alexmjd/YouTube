import logging
from flask import Flask
from flask_restful import Resource, Api
import config
import encoding
from flask_jsonpify import jsonify

app = config.app

apencode = Api(app)

encoder = encoding.Encoding()

apencode.add_resource(encoding.Encoding, '/encoding', methods=['GET', 'POST'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
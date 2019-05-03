#!/bin/bash

# py is an aliases of python3
echo "hello world"
python3 -m venv env

source env/bin/activate

pip install --upgrade pip
pip install flask
pip install requests
pip install connexion
pip install flask_restful
pip install pymysql
pip install flask_jsonpify
pip install cryptography

which python3
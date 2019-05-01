#!/bin/bash

# py is an aliases of python3
echo "hello world"
python3 -m venv env

source env/bin/activate

pip install --upgrade pip
pip install flask
pip install requests

which python3
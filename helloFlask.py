from flask import Flask
print("import flask OK")

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World TPTP"

if __name__ == "__main__":
    app.run()
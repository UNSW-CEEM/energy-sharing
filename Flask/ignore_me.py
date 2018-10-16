import sys
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return "Energy Sharing is Energy Caring (From Flask)"


if __name__ == 'main':
    app.run(host='127.0.0.1', port=5001)

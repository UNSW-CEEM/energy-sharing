from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, rooms, disconnect, join_room, leave_room, close_room

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pleasedonthackme'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

from .endpoints.sockets import SocketsJSON


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('pingServer')
def handle_message(message):
    response_message = "PONG!"
    print('received message: ' + message)
    emit('messageChannel', response_message)
    print('Sent message', response_message)


@socketio.on('connect')
def test_connect():
    print('Connection Attempted')
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('exampleJSON')
def test_example_json(this_json):
    print('JSON Parse Attempted')
    print(this_json)
    SocketsJSON().parse(this_json)


if __name__ == 'main':
    socketio.run(app, debug=True)

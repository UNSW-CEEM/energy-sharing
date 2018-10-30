from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, rooms, disconnect, join_room, leave_room, close_room

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pleasedonthackme'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('pingServer')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('connect')
def test_connect():
    print('Connection Attempted')
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == 'main':
    socketio.run(app, debug=True)

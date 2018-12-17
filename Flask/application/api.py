from threading import Lock
from flask import Flask, render_template, session, request
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit, rooms, disconnect, join_room, leave_room, close_room
from .services import file_service
from .modelling.model_runner import ModelRunner
from .modelling.old_model_parameters import ModelParameters
from .modelling.model_interface import ModelInterface
from .modelling.interfaces.model_parameters import ModelParameters

file_service = file_service.OSFileService()


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pleasedonthackme'

cors = CORS(app, resources={r'/*': {"origins": '*'}})

socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

# File upload endpoint, based on code here:
# http://flask.pocoo.org/docs/0.12/patterns/fileuploads/


@app.route('/upload', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part

        new_file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if new_file.filename == '':
            print("No file selected.")
        if new_file and file_service.valid_file(new_file.filename):
            # filename = secure_filename(file.filename)
            file_service.save(new_file)
            return "<h1>Upload Success: "+new_file.filename+"</h1>"
            
            # return redirect( url_for('uploaded_file',  filename=filename))
    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <p><input type=file name=file>
            <input type=submit value=Upload>
        </form>
        '''


@socketio.on('upload_test')
def upload_test(data):
    print("Received a file")
    print(data)


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('pingServer')
def handle_message(message):
    response_message = "PONG! this is luke"
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
    # SocketsJSON().parse(this_json)


@socketio.on('get_solar_files')
def test_get_solar_files():
    data = file_service.list_solar_files()
    emit('filesChannel', {"key": "solar_files_list", "data": data})


@socketio.on('get_load_files')
def test_get_load_files():
    data = file_service.list_load_files()
    emit('filesChannel', {"key": "load_files_list", "data": data})


@socketio.on('run_model')
def test_run_sim(params):
    # '''Test Code After This'''
    # print(params)
    mi = ModelInterface()
    mi.load(params)
    mi.run(status_callback)

    results = False
    # Show an initialising message while the model gets started.
    status_callback("Initialising Server")

    # Start the process of modelling
    # my_model = ModelRunner()
    # my_params = ModelParameters(params)
    # my_model.load_parameters(my_params)
    # results = my_model.run(status_callback)

    # Send (some) results back to the front end.
    emit('sim_channel', {"data": results})
    status_callback("Modelling Complete")


@socketio.on('run_test_model')
def another_test_run_sim(params):
    status_callback("Running Test Model Interface")
    mp = ModelParameters()
    print("No params coming through!", params)
    mp.load(params)
    emit('sim_channel', {"data": False})


def status_callback(message):
    # my_status = "Status: " + message
    emit('status_channel',
         {
             "data": {
                 "message": message
             }
         }
    )


if __name__ == 'main':
    socketio.run(app, debug=True)

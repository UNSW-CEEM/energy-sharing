from threading import Lock
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from .services import file_service
from .modelling.ui_interfaces.parameters import Parameters as Ui_Parameters

file_service = file_service.OSFileService()

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pleasedonthackme'

cors = CORS(app, resources={r'/*': {"origins": '*'}})

socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

# Create a model parameters object and load up defaults.
mp = Ui_Parameters()


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

# File upload endpoint, based on code here:
# http://flask.pocoo.org/docs/0.12/patterns/fileuploads/


@app.route('/upload/solar_data', methods=['GET', 'POST', 'OPTIONS'])
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
            file_service.save(new_file, "solar_data")
            return "<h1>Upload Success: "+new_file.filename+"</h1>"

    else:
        return ''''''


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
def get_solar_files():
    data = file_service.list_solar_files()
    emit('filesChannel', {"key": "solar_files_list", "data": data})


@socketio.on('get_load_files')
def get_load_files():
    data = file_service.list_load_files()
    emit('filesChannel', {"key": "load_files_list", "data": data})


@socketio.on('get_solar_profiles')
def get_solar_profiles(filename):
    data = file_service.list_solar_profiles(filename)
    emit('profilesChannel', {"key": "solar_profiles_list", "data": data})


@socketio.on('get_load_profiles')
def get_solar_profiles(filename):
    data = file_service.list_load_profiles(filename)
    emit('profilesChannel', {"key": "load_profiles_list", "data": data})


@socketio.on('save_config')
def save_config(page_name, filename, data, additional_headers=None):
    status_callback("Saving participants configuration file")
    result = file_service.save_config(page_name, filename, data, additional_headers)
    if result:
        status_callback("Saving configuration file successful")


@socketio.on('load_config')
def load_config(page_name, filename):
    channel, data = file_service.load_config(page_name, filename)
    if channel and data:
        emit(channel, data)
        status_callback("Configuration file loaded")


@socketio.on('load_participants_config')
def load_config(page_name, filename):
    channel, data = file_service.load_participants_config(page_name, filename)
    if channel and data:
        emit(channel, data)
        status_callback("Configuration file loaded")


@socketio.on('run_model')
def test_run_sim(params):
    status_callback("Running Test Model Interface")
    # Recreate the defaults between the requests while testing
    mp.load_defaults()

    # Overwrite defaults with UI values.
    mp.load(params)
    mp.create_objects()
    results = mp.run(status_callback)

    emit('chart_results_channel', {"data": results})
    status_callback("Modelling Complete")


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

from threading import Lock
from flask import Flask, Blueprint,render_template, request, send_file
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from .services import file_service
from .modelling.ui_interfaces.parameters import Parameters as Ui_Parameters
import os

file_service = file_service.OSFileService()

async_mode = None

app = Flask(__name__, static_folder='dist')
app.config['SECRET_KEY'] = 'pleasedonthackme'

cors = CORS(app, resources={r'/*': {"origins": '*'}})

socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

# Create a model parameters object and load up defaults.
mp = Ui_Parameters()


client_bp = Blueprint('client_app', __name__,
                      url_prefix='',
                      static_url_path='',
                      static_folder='../dist/',
                      template_folder='../dist/',
                      )
app.register_blueprint(client_bp)


@app.route('/')
def index():
    dist_dir = '../dist'
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)
    # return render_template('index.html', async_mode=socketio.async_mode)

# File upload endpoint, based on code here:
# http://flask.pocoo.org/docs/0.12/patterns/fileuploads/


@app.route('/upload/solar_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def upload_solar_file():
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


@app.route('/upload/load_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def upload_load_file():
    if request.method == 'POST':
        # check if the post request has the file part

        new_file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if new_file.filename == '':
            print("No file selected.")

        if new_file and file_service.valid_file(new_file.filename):
            file_service.save(new_file, "load_data")
            return "<h1>Upload Success: "+new_file.filename+"</h1>"

    else:
        return ''''''


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
    emit('profilesChannel', {"key": "solar_profiles_options", "data": data})


@socketio.on('get_load_profiles')
def get_solar_profiles(filename):
    data = file_service.list_load_profiles(filename)
    emit('profilesChannel', {"key": "load_profiles_options", "data": data})


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

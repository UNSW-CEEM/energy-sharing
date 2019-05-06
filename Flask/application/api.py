from threading import Lock
from flask import Flask, Blueprint,render_template, request, send_file
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from .services import file_service
from .modelling.ui_interfaces.parameters import Parameters as Ui_Parameters
import os
import io
import zipfile
import pathlib
import pendulum
import json


file_service = file_service.OSFileService()

# async_mode = None
async_mode = 'threading'
# async_mode = 'eventlet'

app = Flask(__name__, static_folder='dist')
app.config['SECRET_KEY'] = 'pleasedonthackme'

cors = CORS(app, resources={r'/*': {"origins": '*'}})

socketio = SocketIO(app, async_mode = async_mode, engineio_logger=False, async_handlers=True)
thread = None
thread_lock = Lock()

# Create a model parameters object and load up defaults.



client_bp = Blueprint('client_app', __name__,
                      url_prefix='',
                      static_url_path='',
                      static_folder='dist/',
                      template_folder='dist/',
                      )
app.register_blueprint(client_bp)

num_disconnects = 0
num_connects = 0

LAST_MESSAGE = "Official Last Message"
LAST_MESSAGE_TIME = pendulum.now()

@app.route('/')
def index():
    dist_dir = 'dist'
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

@app.route('/download/luomi', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def download_luomi():
    if request.method == 'GET':
        # check if the post request has the file part
        base_path = os.path.join('application','modelling', 'data', 'luomi', 'output')  
        base_path = pathlib.Path(base_path)
        
        data = io.BytesIO()
        with zipfile.ZipFile(data, mode='w') as z:
            for f_name in base_path.iterdir():
                z.write(f_name)
        data.seek(0)
        return send_file(
            data,
            mimetype='application/zip',
            as_attachment=True,
            attachment_filename='data.zip'
        )



@socketio.on('connect')
def test_connect():
    print('Connection Attempted')
    global num_connects
    num_connects += 1
    emit('my response', {'data': 'Connected'})
    status_callback("Connection Reset")


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    global num_disconnects
    num_disconnects += 1
    status_callback('ERROR: Client was Disconnected')
    


@socketio.on('exampleJSON')
def test_example_json(this_json):
    print('JSON Parse Attempted')
    # SocketsJSON().parse(this_json)


@socketio.on('get_solar_files')
def get_solar_files():
    data = file_service.list_solar_files()
    emit('filesChannel', {"key": "solar_files_list", "data": data})

@socketio.on('get_solar_dates')
def get_solar_dates():
    dates = file_service.list_solar_start_end()
    emit('filesChannel', {"key": "solar_dates", "data": dates})

@socketio.on('get_load_dates')
def get_load_dates():
    dates = file_service.list_load_start_end()
    emit('filesChannel', {"key": "load_dates", "data": dates})

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

@socketio.on('get_solar_timeseries')
def get_solar_timeseries(filename):
    data = file_service.get_solar_timeseries(filename)
    # print("Retrieving solar timeseries", data)
    emit('filesChannel', {"key": "solar_timeseries", "data": data})

@socketio.on('get_load_timeseries')
def get_load_timeseries(filename):
    data = file_service.get_load_timeseries(filename)
    # print("Retrieving load timeseries", data)
    emit('filesChannel', {"key": "load_timeseries", "data": data})

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
    emit('status_channel',{'data':{'status':'running'}})
    
    # print([key for key in params])
    # print("Data Sources", params['model_data_sources'])
    # print("Participants", params['model_participants'])
    # Recreate the defaults between the requests while testing
    # mp.load_defaults()

    # Overwrite defaults with UI values.
    # print("api/test_run_sim()",params)
    print("api/test_run_sim()",json.dumps(params, indent=1))

    mp = Ui_Parameters()
    mp.load(params)
    mp.create_objects()
    results = mp.run(status_callback)
    emit('status_channel',{'data':{'status':'finished'}})
    emit('chart_results_channel', {"data": results})
    status_callback("Modelling Complete")



def status_callback(message):
    # my_status = "Status: " + message
    # print("--- Status Callback", message)
    # print("Status Callback - num disconnects", num_disconnects)
    # print("Status Callback - num connects", num_connects)
    global LAST_MESSAGE
    global LAST_MESSAGE_TIME
    # print("Last Message", LAST_MESSAGE)
    # print("--- Status Callback", message)
    if message != LAST_MESSAGE and LAST_MESSAGE_TIME < pendulum.now().subtract(seconds=0.1):
        LAST_MESSAGE = message
        # last_message = message
        LAST_MESSAGE_TIME = pendulum.now()
        # print("--- Status Callback", message)
        
        emit('status_message_channel',
            {
                "data": {
                    "message": message
                }
            }
        )
       
    
    


if __name__ == 'main':
    socketio.run(app, debug=True)

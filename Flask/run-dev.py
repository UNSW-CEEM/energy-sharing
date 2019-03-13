#!/usr/bin/python
import os
import sys
print("Starting Application - Leave this Print In")

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    running_mode = 'Frozen/executable'
else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive (e.g. 'python myapp.py')"
    except NameError:
        application_path = os.getcwd()
        running_mode = 'Interactive'



print('Running mode:', running_mode)
print('  Appliction path  :', application_path)

APPLICATION_PATH = application_path


# BASE_DIR_NAME = os.path.join(os.getcwd(),"application", "modelling", "data")
print("Current directory:",os.getcwd() )
from application import app
app.config.base_path = application_path
app.run(debug=True)

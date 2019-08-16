# replaced with morePVs_reloaded
import json
from application.modelling.ui_interfaces.mike import MikeWrapper

def simple_status_callback(message):
    print("Status", message)


with open('mike_params.json') as params_file:
    params = json.load(params_file)
    print(params)
    wrapper = MikeWrapper()
    wrapper.load(params)
    wrapper.create_objects()
    results = wrapper.run(simple_status_callback)
    print(results)
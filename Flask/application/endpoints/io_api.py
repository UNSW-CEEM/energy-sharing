# This is an API to handle Inputs and Output of model parameters.

# This API should handle
#   (2.0) pushing the form fields to the front end to populate the page dropdowns etc??
#   (2.0) parsing of model parameters and returning errors.

#   (1.0) saving of model parameters


class SocketsJSON:
    def __init__(self):
        output_data = {
            "state": {
                "default_value": {
                    "default_value": ""
                },
                "model": {
                    "simulation": "",
                    "network_type": "",
                },
                "data": {

                },
                "participants": {

                },
                "tariffs": {

                },
                "central_solar": {
                    "data_source": "",
                    "sharing_algorithm": "",
                },
                "central_battery": {
                    "dispatch_algorithm": "",
                    "capacity": "",
                }
            }
        }

    def parse(self, data):
        print(data)
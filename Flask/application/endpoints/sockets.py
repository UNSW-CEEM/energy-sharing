


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
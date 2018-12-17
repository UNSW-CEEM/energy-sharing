class Tariffs:
    def __init__(self, data_dir):
        self.data_dir = data_dir

        self.tariffs = []

    def load(self, inputs):
        for each in inputs:
            row = each["row_inputs"]
            parameters = {}
            for each_dict in row:
                # print(each_dict, "\n")
                parameters[each_dict["name"]] = (each_dict["value"])
            # print(parameters, "\n")
            self.tariffs.append(Tariff(**parameters))


class Tariff:
    def __init__(self,
                 tariff_type=None,
                 tariff_name=None,
                 fit_input=None,
                 peak_price=None,
                 shoulder_price=None,
                 off_peak_price=None):

        self.tariff_type = tariff_type
        self.tariff_name = tariff_name,
        self.fit_input = fit_input,
        self.peak_price = peak_price,
        self.shoulder_price = shoulder_price,
        self.off_peak_price = off_peak_price

    def print(self):
        print("Tariff Object Contains: {}, {}, {}".format(self.tariff_type, self.tariff_name, self.peak_price))

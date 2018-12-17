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
    def __init__(
                self,
                tariff_type,
                tariff_name,
                fit_input,
                peak_charge,
                shoulder_charge,
                offpeak_charge,
            ):

        self.tariff_type = tariff_type
        self.tariff_name = tariff_name
        self.fit_input = fit_input
        self.peak_charge = peak_charge
        self.shoulder_charge = shoulder_charge
        self.offpeak_charge = offpeak_charge

        self.print()

    def print(self):
        print("Tariff Object Contains: {}, {}, {}".format(self.tariff_type, self.tariff_name, self.peak_charge))

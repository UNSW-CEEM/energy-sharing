import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const model_parameters = {
    state: {
        "network_name": "Byron",
        "data_dir": "application/modelling/data",
        "output_dir": "application/modelling/test_output",
        "participants_csv": "participant_meta_data.csv",
        "battery_discharge_file": "ui_battery_discharge_window_eg.csv",
        "tariffs": {
            "scheme_name": "Test",
            "retail_tariff_file": "retail_tariffs.csv",
            "duos_file": "duos.csv",
            "tuos_file": "tuos.csv",
            "nuos_file": "nuos.csv",
            "ui_tariff_file": "ui_tariffs_eg.csv",
        }
    },

    mutations: {
        save_server_page(state, payload) {
            state[payload.model_page_name] = payload.data;
        }
    }
};

const frontend_state = {
    state: {

    },

    mutations: {
        save_page(state, payload) {
            state[payload.model_page_name] = payload.data;
        }
    }
};

export const store = new Vuex.Store({
    strict: true,
    modules: {
        model_parameters: model_parameters,
        frontend_state: frontend_state,
    },

    state: {

    },

    getters: {

    },
    mutations: {

    },
});



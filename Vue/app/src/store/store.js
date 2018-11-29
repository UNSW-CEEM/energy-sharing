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
        "tariffs": [
            {"name": "scheme_name", "value": "Test"},
            {"name": "retail_tariff_file", "value": "retail_tariffs.csv"},
            {"name": "duos_file", "value": "duos.csv"},
            {"name": "tuos_file", "value": "tuos.csv"},
            {"name": "nuos_file", "value": "nuos.csv"},
            {"name": "ui_tariff_file", "value": "ui_tariffs_eg.csv"},
        ]
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

const chart_data = {
    state: {

    },

    mutations: {
        save_page(state, payload) {
            state[payload.chart_name] = payload.data;
        }
    }
};

export const store = new Vuex.Store({
    strict: true,
    modules: {
        chart_data: chart_data,
        frontend_state: frontend_state,
        model_parameters: model_parameters,
    },

    state: {

    },

    getters: {

    },
    mutations: {

    },
});



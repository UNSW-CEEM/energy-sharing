import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const model_parameters = {
    state: {

    },

    mutations: {
        save_server_page(state, payload) {
            state[payload.model_page_name] = payload.data;
        }
    }
};

const frontend_state = {
    state: {
        "selected_model": "luomi",
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



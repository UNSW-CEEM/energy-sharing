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



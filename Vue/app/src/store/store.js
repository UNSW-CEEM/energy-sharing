import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

// This is largely (completely?) static and fills outs drop downs etc.
const input_data = {
    namespaced: true,
    state: {
        default_value: {
            default_value: ""
        },
        central_solar: {
            data_source: [
                {id: 0, name: "data0.csv", link: ""},
                {id: 1, name: "data1.csv", link: ""},
                {id: 2, name: "data2.csv", link: ""},
                {id: 3, name: "data3.csv", link: ""},
            ]
        },
        central_battery: {
            dispatch_algorithm: [
                {id: 0, name: "algorithm 1", link: ""},
                {id: 1, name: "algorithm 2", link: ""},
                {id: 2, name: "algorithm 3", link: ""},
                {id: 3, name: "algorithm 4", link: ""},
            ]
        }
    }
};

// This is output/saved data that will be sent to the python/remote server.
const output_data = {
    state: {
        default_value: {
            default_value: ""
        },
        model: {
            simulation:"",
            network_type: "",
        },
        data: {

        },
        participants: {

        },
        tariffs: {

        },
        central_solar: {
            data_source: "",
            sharing_algorithm: "",
        },
        central_battery: {
            dispatch_algorithm: "",
            capacity: "",
        }
    },
}

export const store = new Vuex.Store({
    strict: true,
    modules: {
        input_data :input_data,
        output_data: output_data
    },

    state: {

    },

    getters: {

    },
    mutations: {
        setValue (state, payload) {
            state.output_data[payload.input_page][payload.field_name] = payload.value
        },

        // reducePrice: (state, payload) => {
        //     state.examples.forEach( example => {
        //         example.price -= payload;
        //     });
        // },
    },
    // actions: {
    //     reducePrice: (context, payload) => {
    //         context.commit('reducePrice', payload)
    //     }
    // }
});



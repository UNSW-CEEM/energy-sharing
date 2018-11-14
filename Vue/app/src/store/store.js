import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

// This is largely (completely?) static and fills outs drop downs etc.
// TODO: Populate the inputs data from the back end.
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
        },
        model_finance: {
            table_headers: [
                {id: 0, name: "Component"},
                {id: 1, name: "CAPEX"},
                {id: 2, name: "Who Pays"},
                {id: 3, name: "Discount Rate"},
                {id: 4, name: "Amortization"},
                {id: 5, name: "OPEX"},
                {id: 6, name: "Who Pays"},
            ]
        }
    }
};

// This is output/saved data that will be sent to the python/remote server.
// TODO:  All saves, api calls, etc, should come from within the store, mutations, actions getters system
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
        },
        model_finance: {
            table_rows: [
                {
                    id: 0,
                    inputs: [
                            {id: 0, text: "Comp", name: "comp", tag: "NumberInput"},
                            {id: 1, text: "CAP", name: "capex", tag: "NumberInput"},
                            {id: 2, text: "CAP PAY", name: "capex_payer", tag: "TableDropdownInput"},
                            {id: 3, text: "DISC RAT", name: "discount_rate", tag: "NumberInput"},
                            {id: 4, text: "AMORT", name: "amortization", tag: "NumberInput"},
                            {id: 5, text: "OPEX", name: "opex", tag: "NumberInput"},
                            {id: 6, text: "OP PAY", name: "opex_payer", tag: "TableDropdownInput"},
                        ]
                },
            ]
        }
    },
};

//TODO: This could be moved to the main store object. But this is easy and more abstracted so will keep here.
const frontend_state = {
    state: {
        completed_pages: 2,
        total_pages: 9,
    },

    getters: {
        getCompletedPages(state) {
            return state.completed_pages;
        }
    },

    mutations: {

    }
};

export const store = new Vuex.Store({
    strict: true,
    modules: {
        input_data :input_data,
        output_data: output_data,
        frontend_state: frontend_state,
    },

    state: {

    },

    getters: {

    },
    mutations: {
        setValue (state, payload) {
            state.output_data[payload.input_page][payload.field_name] = payload.value
        },

        setTableDropdown (state, payload) {
            state.output_data[payload.input_page][payload.array_name][payload.row_index][payload.field_name] = payload.value
        },

        addRow(state, payload) {
            state.output_data[payload.input_page][payload.field_name].push(payload.row)
        },
    },
});



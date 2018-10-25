import Vue from 'vue'
import Vuex from 'vuex'

import { getField, updateField } from 'vuex-map-fields';

Vue.use(Vuex);

export const store = new Vuex.Store({
    strict: true,
    state: {
        examples: [
            { id: 0, name: "Example 1", price: 10 },
            { id: 1, name: "Example 2", price: 20 },
            { id: 3, name: "Example 3", price: 40 },
            { id: 4, name: "Example 4", price: 80 },
        ],

        saved_data: {
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
            }
        },

        inputs_data: {
            central_solar: {
                data_source: [
                    {id: 0, name: "data0.csv", link: ""},
                    {id: 1, name: "data1.csv", link: ""},
                    {id: 2, name: "data2.csv", link: ""},
                    {id: 3, name: "data3.csv", link: ""},
                ]
            }
        },
    },

    getters: {
        getField,

        examplesGetter: state => {
            var examplesGetter = state.examples.map(example => {
                return {
                    id: example.id,
                    name: 'Getter: ' + example.name,
                    price: example.price,
                }
            });
            return examplesGetter;
        }
    },
    mutations: {
        updateField,

        reducePrice: (state, payload) => {
            state.examples.forEach( example => {
                example.price -= payload;
            });
        },

        // SET_INPUT_VALUE: (state, id) => {
        //     var updated = state.example_inputs.find(example => example.id === id);
        //     updated.value = "This got set";
        // }

    },
    actions: {
        reducePrice: (context, payload) => {
            context.commit('reducePrice', payload)
        }
    }
});

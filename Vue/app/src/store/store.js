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

        example_inputs: [
            {
                id: 0,
                class:"text_input",
                type:"text",
                placeholder:"FROM STORE",
                data_model:"this_title",
                value: ""
            },
            {
                id: 1,
                class:"text_input",
                type:"text",
                placeholder:"ALSO FROM STORE",
                data_model:"another_title",
                value: ""
            },
        ],
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

import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export const store = new Vuex.Store({
    strict: true,
    state: {
        examples: [
            { id: 0, name: "Example 1", price: 10 },
            { id: 1, name: "Example 2", price: 20 },
            { id: 3, name: "Example 3", price: 40 },
            { id: 4, name: "Example 4", price: 80 },
        ]
    },

    getters: {
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
        reducePrice: (state, payload) => {
            state.examples.forEach( example => {
                example.price -= payload;
            });
        }
    },
    actions: {
        reducePrice: (context, payload) => {
            context.commit('reducePrice', payload)
        }
    }
});

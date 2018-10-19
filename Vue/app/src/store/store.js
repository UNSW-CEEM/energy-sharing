import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = {
    state: {
        examples: [
            {
                id: 0,
                name: "Example 1"
            },
            {
                id: 1,
                name: "Example 2"
            },
            {
                id: 3,
                name: "Example 3"
            },
            {
                id: 4,
                name: "Example 4"
            }
        ]
    }
}
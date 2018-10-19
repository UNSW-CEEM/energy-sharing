import Vue from 'vue'
import Router from 'vue-router'

import About from './pages/About.vue'
import Contact from './pages/Contact.vue'
import Home from './pages/Home.vue'
import Inputs from './pages/Inputs.vue'

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/about',
            name: 'about',
            // route level code-splitting
            // this generates a separate chunk (about.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: () => import(/* webpackChunkName: "about" */ './pages/About.vue')
        },
        {
            path: '/contact',
            name: 'contact',
            component: Contact
        },
        {
            path: '/data',
            name: 'data',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/Data.vue')
        },
        {
            path: '/inputs',
            name: 'inputs',
            component: Inputs
        },

        {
            path: '/model',
            name: 'model',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/Model.vue')
        },
    ]
})

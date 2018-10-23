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
        {
            path: '/central_battery',
            name: 'central_battery',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/CentralBattery.vue')
        },
        {
            path: '/central_solar',
            name: 'central_solar',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/CentralSolar.vue')
        },
        {
            path: '/financing',
            name: 'financing',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/Financing.vue')
        },
        {
            path: '/participants',
            name: 'participants',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/Participants.vue')
        },
        {
            path: '/review',
            name: 'review',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/Review.vue')
        },
        {
            path: '/tariffs',
            name: 'tariffs',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/Tariffs.vue')
        },
    ]
})

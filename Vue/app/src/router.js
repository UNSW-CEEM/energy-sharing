import Vue from 'vue'
import Router from 'vue-router'

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
            path: '/data_load',
            name: 'data_load',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/ModelDataLoad.vue')
        },
        {
            path: '/data_solar',
            name: 'data_solar',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/ModelDataSolar.vue')
        },
        {
            path: '/inputs',
            name: 'inputs',
            component: Inputs
        },
        {
            path: '/model',
            name: 'model',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/ModelSelection.vue')
        },
        {
            path: '/central_battery',
            name: 'central_battery',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/ModelBattery.vue')
        },
        {
            path: '/central_solar',
            name: 'central_solar',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/ModelSolar.vue')
        },
        {
            path: '/financing',
            name: 'financing',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/ModelFinancing.vue')
        },
        {
            path: '/participants',
            name: 'participants',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/ModelParticipants.vue')
        },
        {
            path: '/review',
            name: 'review',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/ModelReview.vue')
        },
        {
            path: '/results',
            name: 'results',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/ModelResults.vue')
        },
        {
            path: '/tariffs',
            name: 'tariffs',
            component: () => import(/* webpackChunkName: "model" */ './pages/inputs/ModelTariffs.vue')
        },
    ]
})

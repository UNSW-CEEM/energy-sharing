import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/defaults/Home.vue'
import InputMain from './views/input_main/InputMain.vue'

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
            component: () => import(/* webpackChunkName: "about" */ './views/defaults/About.vue')
        },
        {
            path: '/model',
            name: 'model',
            component: () => import(/* webpackChunkName: "model" */ './views/input_main/input_pages/Model.vue')
        },
        {
            path: '/data',
            name: 'data',
            component: () => import(/* webpackChunkName: "model" */ './views/input_main/input_pages/Data.vue')
        },
    ]
})

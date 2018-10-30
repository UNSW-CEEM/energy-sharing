import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { store } from './store/store'

import Vuelidate from 'vuelidate'
Vue.use(Vuelidate);

import socketio from 'socket.io-client';
import VueSocketIO from 'vue-socket.io';

export const SocketInstance = socketio('http://localhost:5000/');
Vue.use(VueSocketIO, SocketInstance);

Vue.config.productionTip = false;

new Vue({
    store,
    router,
    render: h => h(App)
}).$mount('#app')

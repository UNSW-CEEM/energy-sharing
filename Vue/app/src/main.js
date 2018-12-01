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

import VModal from 'vue-js-modal'
Vue.use(VModal)

import { library } from '@fortawesome/fontawesome-svg-core'
import { faCoffee, faStroopwafel, faNetworkWired, faPlaneDeparture, faTable, faUser, faExchangeAlt, faSolarPanel, faBatteryFull, faMoneyCheckAlt, faSearch, faPoll } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faCoffee)
library.add(faStroopwafel)
library.add(faNetworkWired)
library.add(faPlaneDeparture)
library.add(faTable)
library.add(faUser)
library.add(faExchangeAlt)
library.add(faSolarPanel)
library.add(faBatteryFull)
library.add(faMoneyCheckAlt)
library.add(faSearch)
library.add(faPoll)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false;

new Vue({
    store,
    router,
    render: h => h(App)
}).$mount('#app')

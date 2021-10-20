import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import store from './components/store';
import axios from 'axios';
import VueAxios from 'vue-axios';
import { LMap, LTileLayer, LMarker } from 'vue2-leaflet';
// import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'leaflet/dist/leaflet.css';

// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false
Vue.use(VueAxios, axios);
// Vue.use(BootstrapVue)
// Vue.use(IconsPlugin)
Vue.component('l-map', LMap);
Vue.component('l-tile-layer', LTileLayer);
Vue.component('l-marker', LMarker);

new Vue({
  store,
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')

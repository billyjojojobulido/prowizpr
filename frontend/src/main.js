import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue'
import axios from 'axios';
import locale from "../node_modules/element-ui/lib/locale/lang/en.js";
import router from "./router";
import store from "./store";

import VueCookies from "vue-cookies";



Vue.config.productionTip = false
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
Vue.prototype.$axios = axios
Vue.use(ElementUI, {locale})
Vue.use(VueCookies);

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App),
}).$mount('#app')

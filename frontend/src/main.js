import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import Select2 from 'vue3-select2-component';

import '@/assets/css/theme.bundle.css'
import '@/assets/css/libs.bundle.css'

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:8000';

const app = createApp(App).use(store).use(router)
app.component('Select2', Select2)
app.mount('#app')

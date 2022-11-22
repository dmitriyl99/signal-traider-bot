import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import Select2 from 'vue3-select2-component';
import VueAwesomePaginate from "vue-awesome-paginate";
import "vue-awesome-paginate/dist/style.css";

import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';

import '@/assets/css/theme.bundle.css'
import '@/assets/css/libs.bundle.css'

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:8000';

const app = createApp(App).use(store).use(router)
app.component('Select2', Select2)
app.use(VueSweetalert2).use(VueAwesomePaginate);
app.mount('#app')

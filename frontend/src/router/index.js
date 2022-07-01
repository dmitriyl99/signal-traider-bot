import { createRouter, createWebHashHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue';
import UsersList from "../views/Users/UsersList";
import Login from "../views/auth/Login";

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Dashboard,
    meta: {
      layout: 'AppLayoutAdmin'
    }
  },
  {
    path: '/users',
    name: 'UsersList',
    component: UsersList,
    meta: {
      layout: 'AppLayoutAdmin'
    }
  },
  {
    path: '/auth/login',
    name: 'auth.login',

    component: Login
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router

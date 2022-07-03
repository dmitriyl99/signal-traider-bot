import {createRouter, createWebHashHistory} from 'vue-router'
import Dashboard from '../views/Dashboard.vue';
import UsersList from "../views/Users/UsersList";
import PaymentsList from "../views/payments/PaymentsList";
import ListSignals from "../views/Signals/ListSignals";
import CreateSignal from "../views/Signals/CreateSignal";
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
        path: '/payments',
        name: 'PaymentsList',
        component: PaymentsList,
        meta: {
            layout: 'AppLayoutAdmin'
        }
    },
    {
        path: '/signals',
        name: 'ListSignals',
        component: ListSignals,
        meta: {
            layout: 'AppLayoutAdmin'
        },
    },
    {
        path: '/signals/create',
        component: CreateSignal,
        name: 'CreateSignal',
        meta: {
            layout: 'AppLayoutAdmin'
        },
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

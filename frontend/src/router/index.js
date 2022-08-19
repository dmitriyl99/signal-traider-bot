import {createRouter, createWebHashHistory} from 'vue-router'
import Dashboard from '../views/Dashboard.vue';
import UsersList from "../views/Users/UsersList";
import CreateUser from "../views/Users/CreateUser";
import PaymentsList from "../views/payments/PaymentsList";
import ListSignals from "../views/Signals/ListSignals";
import CreateSignal from "../views/Signals/CreateSignal";
import Login from "../views/auth/Login";
import auth from "./middleware/auth";
import guest from "./middleware/guest";
import store from '../store'
import middlewarePipeline from "./middlewarePipeline";

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Dashboard,
        meta: {
            layout: 'AppLayoutAdmin',
            middleware: [
                auth
            ]
        }
    },
    {
        path: '/users',
        name: 'UsersList',
        component: UsersList,
        meta: {
            layout: 'AppLayoutAdmin',
            middleware: [
                auth
            ]
        }
    },
    {
        path: '/users/create',
        name: 'CreateUser',
        component: CreateUser,
        meta: {
            layout: 'AppLayoutAdmin',
            middleware: [
                auth
            ]
        }
    },
    {
        path: '/payments',
        name: 'PaymentsList',
        component: PaymentsList,
        meta: {
            layout: 'AppLayoutAdmin',
            middleware: [
                auth
            ]

        }
    },
    {
        path: '/signals',
        name: 'ListSignals',
        component: ListSignals,
        meta: {
            layout: 'AppLayoutAdmin',
            middleware: [
                auth
            ]
        },
    },
    {
        path: '/signals/create',
        component: CreateSignal,
        name: 'CreateSignal',
        meta: {
            layout: 'AppLayoutAdmin',
            middleware: [
                auth
            ]
        },
    },
    {
        path: '/auth/login',
        name: 'auth.login',
        component: Login,

        meta: {
            middleware: [
                guest
            ]
        }
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    if (!to.meta.middleware) {
        return next()
    }
    const middleware = to.meta.middleware;
    const context = {
        to, from, next, store
    }
    return middleware[0]({...context, next: middlewarePipeline(context, middleware, 1)})
})

export default router

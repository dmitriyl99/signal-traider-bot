import {createRouter, createWebHashHistory} from 'vue-router'
import Dashboard from '../views/Dashboard.vue';
import UsersList from "../views/Users/UsersList";
import CreateUser from "../views/Users/CreateUser";
import UpdateUser from "../views/Users/UpdateUser";
import PaymentsList from "../views/payments/PaymentsList";
import ListSignals from "../views/Signals/ListSignals";
import DistributionsList from "../views/Distributions/DistributionsList";
import CreateDistribution from "../views/Distributions/CreateDistribution";
import SendReplySignal from "../views/Signals/SendReplySignal";
import CreateSignal from "../views/Signals/CreateSignal";
import CurrencyPairsList from "../views/currency-pairs/CurrencyPairsList";
import UtmList from "../views/utm/UtmList";
import AdminUsersList from "../views/AdminUsers/AdminUsersList";
import AdminUserCreate from "../views/AdminUsers/AdminUserCreate";
import AdminUserEdit from "../views/AdminUsers/AdminUserEdit";
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
        path: '/users/:id',
        name: 'UpdateUser',
        component: UpdateUser,
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
        path: '/distributions',
        name: 'ListDistributions',
        component: DistributionsList,
        meta: {
            layout: 'AppLayoutAdmin',
            middleware: [
                auth
            ]
        },
    },
    {
        path: '/distributions/create',
        name: 'CreateDistribution',
        component: CreateDistribution,
        meta: {
            layout: 'AppLayoutAdmin',
            middleware: [
                auth
            ]
        },
    },
    {
        path: '/signals/:id/reply',
        name: 'signals.reply',
        component: SendReplySignal,
        meta: {
            layout: 'AppLayoutAdmin',
            middleware: [
                auth
            ]
        }
    },
    {
        path: '/currency-pairs',
        component: CurrencyPairsList,
        name: 'CurrencyPairsList',
        meta: {
            layout: 'AppLayoutAdmin',
            middleware: [
                auth
            ]
        }
    },
    {
        path: '/utm',
        component: UtmList,
        name: 'UtmList',
        meta: {
            layout: 'AppLayoutAdmin',
            middleware: [
                auth
            ]
        }
    },
    {
        path: '/admin-users',
        component: AdminUsersList,
        name: 'admin-users.list',
        meta: {
            layout: 'AppLayoutAdmin',
            middleware: [
                auth
            ]
        }
    },
    {
        path: '/admin-users/create',
        component: AdminUserCreate,
        name: 'admin-users.create',
        meta: {
            layout: 'AppLayoutAdmin',
            middleware: [
                auth
            ]
        }
    },
    {
        path: '/admin-users/:id',
        component: AdminUserEdit,
        name: 'admin-users.edit',
        meta: {
            layout: 'AppLayoutAdmin',
            middleware: [
                auth
            ]
        }
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

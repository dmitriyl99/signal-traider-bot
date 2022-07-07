export default function auth({ next, store }) {
    if (!store.getters.isLoggedIn) {
        return next({
            name: 'auth.login'
        })
    }

    return next()
}
export default function guest({ next, store }) {
    if (store.getters.isLoggedIn) {
        return next({
            name: 'Home'
        })
    }

    return next()
}
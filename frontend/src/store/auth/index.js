const authModule = {
    state: () => ({
        jwt_token: null,
        current_user: null
    }),
    mutations: {

    },
    actions: {

    },
    getters: {
        jwtToken(state) {
            return state.jwt_token
        },
        currentUser(state) {
            return state.current_user
        }
    }
};

export default authModule;
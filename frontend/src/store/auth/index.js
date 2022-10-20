import authApi from "../../api/authApi";

const authModule = {
    state: () => ({
        jwt_token: loadValue('jwt_token'),
        current_user: loadObject('current_user'),
        permissions: loadObject('permissions'),
        roles: loadObject('roles')
    }),
    mutations: {
        setJwtToken(state, {jwtToken}) {
            state.jwt_token = jwtToken;
            saveValue('jwt_token', jwtToken);
        },
        setCurrentUser(state, {currentUser}) {
            state.current_user = currentUser;
            saveObject('current_user', currentUser);
        },

        setPermissions(state, {permissions}) {
            state.permissions = permissions;
            saveObject('permissions', permissions)
        },

        setRoles(state, {roles}) {
            state.roles = roles;
            saveObject('roles', roles)
        },

        logout(state) {
            state.jwt_token = null;
            state.current_user = null;
            state.permissions = null;
            state.roles = null;
            localStorage.removeItem('jwt_token');
            localStorage.removeItem('current_user')
            localStorage.removeItem('permissions');
            localStorage.removeItem('roles');
        }
    },
    actions: {
        login(context, {username, password}) {
            return new Promise((resolve, reject) => {
                authApi.getJwtToken(username, password).then(response => {
                    let accessToken = response.data.access_token;
                    context.commit('setJwtToken', {jwtToken: accessToken})
                    resolve(true);
                }, error => {
                    reject(error)
                })
            })
        },
        fetchUser(context) {
            let accessToken = context.state.jwt_token;
            authApi.getCurrentUser(accessToken).then(response => {
                context.commit('setCurrentUser', {currentUser: response.data})
                authApi.getPermissions(accessToken).then(response => {
                    context.commit('setPermissions', {permissions: response.data})
                    authApi.getRoles(accessToken).then(response => {
                        context.commit('setRoles', {roles: response.data})
                    })
                })
            })

            return accessToken;
        },
        logout(context) {
            context.commit('logout')
        }
    },
    getters: {
        jwtToken(state) {
            return state.jwt_token
        },
        currentUser(state) {
            return state.current_user
        },
        isLoggedIn(state) {
            return state.jwt_token != null;
        },
        userPermissions(state) {
            return state.permissions
        },
        userRoles(state) {
            return state.roles
        }
    }
};

function saveValue(key, value) {
    localStorage.setItem(key, value);
}

function saveObject(key, object) {
    localStorage.setItem(key, JSON.stringify(object));
}

function loadValue(key) {
    return localStorage.getItem(key);
}

function loadObject(key) {
    return JSON.parse(localStorage.getItem(key));
}

export default authModule;
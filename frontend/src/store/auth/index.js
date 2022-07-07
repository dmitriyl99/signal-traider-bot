import authApi from "../../api/authApi";

const authModule = {
    state: () => ({
        jwt_token: loadValue('jwt_token'),
        current_user: loadObject('current_user')
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

        logout(state) {
            state.jwt_token = null;
            state.current_user = null;
            localStorage.removeItem('jwt_token');
            localStorage.removeItem('current_user')
        }
    },
    actions: {
        login(context, {username, password}) {
            return new Promise((resolve, reject) => {
                authApi.getJwtToken(username, password).then(response => {
                    let accessToken = response.data.access_token;
                    context.commit('setJwtToken', {jwtToken: accessToken})
                    authApi.getCurrentUser(accessToken).then(response => {
                        context.commit('setCurrentUser', {currentUser: response.data})
                        resolve(true)
                    }, error => {
                        reject(error)
                    })
                }, error => {
                    reject(error)
                })
            })
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
            return state.jwt_token != null && state.current_user != null
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
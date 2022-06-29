import authApi from "../../api/authApi";

const authModule = {
    state: () => ({
        jwt_token: loadValue('jwt_token'),
        current_user: loadObject('current_user')
    }),
    mutations: {
        login(state, {jwtToken, currentUser}) {
            state.jwt_token = jwtToken;
            state.current_user = currentUser;

            saveValue('jwt_token', jwtToken);
            saveObject('current_user', currentUser);
        }
    },
    actions: {
        login(context, {username, password}) {
            return new Promise((resolve, reject) => {
                authApi.getJwtToken(username, password).then(response => {
                    let accessToken = response.data.access_token;
                    authApi.getCurrentUser(accessToken).then(response => {
                        context.commit('login', {jwtToken: accessToken, currentUser: response.data})
                        resolve(true)
                    }, error => {
                        reject(error)
                    })
                }, error => {
                    reject(error)
                })
            })
        }
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
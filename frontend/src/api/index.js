import axios from 'axios'
import router from '../router'
import store from '../store'

const apiInstance = axios.create({
    baseURL: 'http://localhost:8000/api/'
})

apiInstance.interceptors.response.use(function (response) {
    return response
}, function (error) {
    if (error.response.status === 401) {
        store.dispatch('logout')
        router.push({ name: 'Login' })
    }
    return Promise.reject(error)
})

apiInstance.interceptors.request.use(config => {
    config.headers['Authorization'] = `Bearer ${store.getters.jwtToken}`
    return config
}, error => {
    return Promise.reject(error)
})

export default apiInstance;
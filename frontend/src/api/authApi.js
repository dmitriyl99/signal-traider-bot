import apiInstance from "./index";

function getJwtToken(username, password) {
    return apiInstance.post('/auth/token', { username, password })
}

function getCurrentUser(token) {
    return apiInstance.get('/auth/me', {
        headers: {'Authorization': `Bearer ${token}`}
    })
}

export default {
    getJwtToken,
    getCurrentUser
}
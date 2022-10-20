import apiInstance from "./index";

function getJwtToken(username, password) {
    return apiInstance.post('/auth/token', { username, password })
}

function getCurrentUser(token) {
    return apiInstance.get('/auth/me', {
        headers: {'Authorization': `Bearer ${token}`}
    })
}

function getPermissions(token) {
    return apiInstance.get('/auth/me/permissions', {
        headers: {'Authorization': `Bearer ${token}`}
    })
}

function getRoles(token) {
    return apiInstance.get('/auth/me/roles', {
        headers: {'Authorization': `Bearer ${token}`}
    })
}

export default {
    getJwtToken,
    getCurrentUser,
    getPermissions,
    getRoles
}
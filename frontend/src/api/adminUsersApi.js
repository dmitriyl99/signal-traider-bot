import apiInstance from "./index";


function getAdminUsersList() {
    return apiInstance.get('/admin-users')
}

function createAdminUser(username, password, password_confirmation, roles, permissions) {
    return apiInstance.post('/admin-users', {username, password, password_confirmation, roles, permissions});
}

function getAdminUserById(adminUserId) {
    return apiInstance.get(`admin-users/${adminUserId}`)
}

function changePassword(adminUserId, password, password_confirmation) {
    return apiInstance.post(`admin-users/${adminUserId}/change-password`, {password, password_confirmation})
}

export default {
    getAdminUsersList,
    createAdminUser,
    getAdminUserById,
    changePassword
}

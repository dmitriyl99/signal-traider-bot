import apiInstance from "./index";


function getAdminUsersList() {
    return apiInstance.get('/admin-users')
}

export default {
    getAdminUsersList
}

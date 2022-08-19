import apiInstance from "./index";

function getUsersList() {
    return apiInstance.get('/users')
}

function saveUser(
    name, phone, subscription_id, subscription_condition_id
) {
    return apiInstance.post('/users', {
        name, phone,
        subscription_id, subscription_condition_id
    })
}

export default {
    getUsersList, saveUser
}
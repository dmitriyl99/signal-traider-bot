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

function getUserById(id) {
    return apiInstance.get(`/users/${id}`);
}

function updateUser(
    id, name, phone, subscription_id, subscription_condition_id
) {
    return apiInstance.put(`/users/${id}`, {
        name, phone, subscription_id, subscription_condition_id
    })
}

export default {
    getUsersList, saveUser, getUserById, updateUser
}
import apiInstance from "./index";

function getUsersList(page = 1) {
    return apiInstance.get(`/users?page=${page}`)
}

function saveUser(
    name, phone, subscription_id, subscription_condition_id, subscription_duration_in_days
) {
    return apiInstance.post('/users', {
        name, phone,
        subscription_id, subscription_condition_id, subscription_duration_in_days
    })
}

function getUserById(id) {
    return apiInstance.get(`/users/${id}`);
}

function updateUser(
    id, name, phone, subscription_id, subscription_condition_id, subscription_duration_in_days
) {
    return apiInstance.put(`/users/${id}`, {
        name, phone, subscription_id, subscription_condition_id, subscription_duration_in_days
    })
}

export default {
    getUsersList, saveUser, getUserById, updateUser
}
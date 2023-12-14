import apiInstance from "./index";

function getUsersList(page = 1, searchQuery = '') {
    return apiInstance.get(`/users/?page=${page}&search=${searchQuery}`)
}

function saveUser(
    name, phone, subscription_id, subscription_condition_id, subscription_duration_in_days
) {
    return apiInstance.post('/users/', {
        name, phone,
        subscription_id, subscription_condition_id, subscription_duration_in_days
    })
}

function getUserById(id) {
    return apiInstance.get(`/users/${id}/`);
}

function updateUser(
    id, name, phone, subscription_id, subscription_condition_id, subscription_duration_in_days
) {
    return apiInstance.put(`/users/${id}/`, {
        name, phone, subscription_id, subscription_condition_id, subscription_duration_in_days
    })
}

function deleteUser(
    id,
) {
    return apiInstance.delete(`/users/${id}/`)
}

export default {
    getUsersList, saveUser, getUserById, updateUser, deleteUser
}
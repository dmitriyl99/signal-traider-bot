import apiInstance from "./index";

function getUsersList(page = 1, searchQuery = '', filter_subscription = '') {
    return apiInstance.get(`/users/`, {params: {search: searchQuery, page: page, filter_subscription: filter_subscription}})
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

function downloadExcel()
{
    return apiInstance.get('/users/excel', {responseType: 'blob'})
}

export default {
    getUsersList, saveUser, getUserById, updateUser, deleteUser, downloadExcel
}
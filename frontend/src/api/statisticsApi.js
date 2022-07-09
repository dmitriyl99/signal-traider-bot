import apiInstance from "./index";


function getUsersStatistics() {
    return apiInstance.get('/dashboard/users');
}

export default {
    getUsersStatistics
}
import apiInstance from "./index";


function getUsersStatistics() {
    return apiInstance.get('/dashboard/users');
}

function getSubscriptionsStatistics() {
    return apiInstance.get('/dashboard/subscriptions');
}

export default {
    getUsersStatistics,
    getSubscriptionsStatistics
}
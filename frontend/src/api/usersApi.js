import apiInstance from "./index";

function getUsersList() {
    return apiInstance.get('/users')
}

export default {
    getUsersList
}
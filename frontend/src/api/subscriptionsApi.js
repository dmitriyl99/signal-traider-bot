import apiInstance from "./index";


function getSubscriptions() {
    return apiInstance.get('/subscriptions/');
}

export default {
    getSubscriptions
}

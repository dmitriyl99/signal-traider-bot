import apiInstance from "./index";

function getPayments() {
    return apiInstance.get('/payments');
}

export default {
    getPayments
}
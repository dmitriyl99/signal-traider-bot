import apiInstance from "./index";

function getCurrencyPairs() {
    return apiInstance.get('/currency-pairs/');
}

function saveCurrentPairs(name) {
    return apiInstance.post('/currency-pairs/', {
        pair_name: name
    })
}

export default {
    getCurrencyPairs, saveCurrentPairs
}
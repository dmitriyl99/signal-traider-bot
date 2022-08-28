import apiInstance from "./index";


function sendSignal(
    currencyPair,
    executionMethod,
    price,
    tr_1,
    tr_2,
    sl
) {
    let payload = {
        currency_pair: currencyPair,
        execution_method: executionMethod,
        price: price * 100,
        tr_1,
        tr_2,
        sl
    }

    return apiInstance.post('/signals', payload);
}

function getAllSignals() {
    return apiInstance.get('/signals');
}

function getSuggestion(currencyPair) {
    return apiInstance.get('/signals/suggestion', {params: {currency_pair: currencyPair}})
}

export default {
    sendSignal, getAllSignals, getSuggestion
}

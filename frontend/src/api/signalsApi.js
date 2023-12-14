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
        price,
        tr_1,
        tr_2,
        sl
    }

    return apiInstance.post('/signals/', payload);
}

function sendReply(signal_id, text) {
    return apiInstance.post(`/signals/${signal_id}/reply/`, {text})
}

function sendCustomMessage(text, files=null, images=null, importance = '0', currency_pair) {
    let formData = new FormData();
    formData.append('text', text);
    formData.append('importance', importance);
    formData.append('currency', currency_pair)
    if (files !== null) {
        Array.from(files).forEach(file => {
            formData.append('files', file);
        })
    }
    if (images !== null) {
        Array.from(images).forEach(image => {
            formData.append('images', image);
        })
    }

    return apiInstance.post('/signals/message/', formData, {headers: {"Content-Type": "multipart/form-data"}});
}

function loadCustomMessages() {
    return apiInstance.get('/signals/message/');
}

function getAllSignals() {
    return apiInstance.get('/signals/');
}

function getSuggestion(currencyPair) {
    return apiInstance.get('/signals/suggestion/', {params: {currency_pair: currencyPair}})
}

export default {
    sendSignal, getAllSignals, getSuggestion, sendCustomMessage, sendReply, loadCustomMessages
}

import apiInstance from "./index";

function getPayments(
    filter_status,
    filter_sum,
    filter_provider,
    filter_duration,
    filter_date_from,
    filter_date_to,
) {
    let params = {
        filter_status,
        filter_provider,
        filter_date_from,
        filter_date_to
    }
    if (filter_duration) {
        params.filter_duration = filter_duration;
    }
    if (filter_sum) {
        params.filter_sum = filter_sum
    }

    return apiInstance.get('/payments/', { params: params });
}

export default {
    getPayments
}
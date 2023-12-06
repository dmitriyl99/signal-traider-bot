import requests
import logging


def convert_usd_to_uzs(amount: int) -> float:
    url = 'https://nbu.uz/en/exchange-rates/json/'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        filtered_data = list(filter(lambda x: x['code'] == 'USD', data))
        if len(filtered_data) > 0:
            return amount * float(filtered_data[0]['cb_price'])

    logging.error(f"Error while getting exchange course: {response.status_code} - {response.json()}")
    default_course = 12280.0

    return amount * default_course

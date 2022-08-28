from typing import Optional

import requests


class TradingViewScanResponse:
    name: str
    price: float
    recommends: float

    def __init__(self, name: str, price: float, recommends: float):
        self.name = name
        self.price = price
        self.recommends = recommends


class TradingViewException(Exception):
    pass


def trading_view_scan(currency_pair_name: str) -> Optional[TradingViewScanResponse]:
    url = 'https://scanner.tradingview.com/forex/scan'
    payload = {
        'symbols': {
            'tickers': [
                f"FX_IDC:{currency_pair_name}"
            ]
        },
        'columns': [
            'name',
            'close',
            'Recommend.All'
        ]
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        response_data = response.json()
        if response_data['totalCount'] > 0:

            return TradingViewScanResponse(
                name=response_data['data'][0]['d'][0],
                price=response_data['data'][0]['d'][1],
                recommends=response_data['data'][0]['d'][2]
            )
        return None

    raise TradingViewException(str(response.content))


from app.config import config

import uuid

from typing import List


class PaymentProvider:
    name: str
    provider_token: str
    params: dict

    def __init__(self, name: str, provider_token: str):
        self.name = name
        self.provider_token = provider_token


def get_payment_providers() -> List[PaymentProvider]:
    available_providers = config.PAYMENT_PROVIDERS
    providers = []
    if 'click' in available_providers:
        providers.append(PaymentProvider(name='Click', provider_token=config.CLICK_PAYMENT_PROVIDER_TOKEN))
    if 'payme' in available_providers:
        providers.append(PaymentProvider(name='Payme', provider_token=config.PAYME_PAYMENT_PROVIDER_TOKEN))
    return providers


def get_payment_provider_by_name(name: str) -> PaymentProvider | None:
    providers = get_payment_providers()
    found_providers = list(filter(lambda provider: provider.name == name, providers))
    if len(found_providers) > 0:
        return found_providers[0]
    return None


def get_click_payment_url(amount: float):
    service_id = config.CLICK_SERVICE_ID
    merchant_id = config.CLICK_MERCHANT_ID
    transaction_param = uuid.uuid4()
    url = f"https://my.click.uz/services/pay?service_id={service_id}&merchant_id={merchant_id}&amount={int(amount)}&transaction_param={transaction_param}"

    return url



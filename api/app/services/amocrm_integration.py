import json
import os

import requests
from amocrm_api import AmoOAuthClient

from app.config import settings
from app.data.models.users import User


class AmoCrmUserType:
    NEW_USER: str = "Зарегистрировался, но не купил подкписку"
    LOST_USER: str = "Не продлил подписку"


class AmoCrmAuthError(Exception):
    pass


def _get_auth_access_token() -> dict:
    if not os.path.exists('masspower_amo_crm_token.json'):
        data = {
            'client_id': settings.amocrm_client_id,
            'client_secret': settings.amocrm_secret_key,
            'grant_type': 'authorization_code',
            'code': settings.amocrm_authorization_code,
            'redirect_uri': settings.amocrm_redirect_uri
        }

        auth_url = f'https://masspower.amocrm.ru/oauth2/access_token'
        response = requests.post(auth_url, json=data)
        response_data = response.json()
        if response.status_code != 200:
            raise AmoCrmAuthError(response_data['hint'])
        refresh_token = response_data['refresh_token']
        access_token = response_data['access_token']

        auth_data = {
            'refresh_token': refresh_token,
            'access_token': access_token
        }

        with open(f'masspower_amo_crm_token.json', 'w') as f:
            json.dump(auth_data, f, indent=2)

        return auth_data

    with open(f'masspower_amo_crm_token.json', 'r') as f:
        auth_data = json.load(f)

    return auth_data


def _get_client() -> AmoOAuthClient:
    auth_data = _get_auth_access_token()
    return AmoOAuthClient(
        access_token=auth_data['access_token'],
        refresh_token=auth_data['refresh_token'],
        crm_url='https://masspower.amocrm.ru/',
        client_id=settings.amocrm_client_id,
        client_secret=settings.amocrm_secret_key,
        redirect_uri=settings.amocrm_redirect_uri,
    )


def add_user_to_catalog(user: User, note_type: str):
    client = _get_client()
    catalog = _get_catalog(client)
    elements = [
        {
            "name": user.name,
            "custom_fields_values": [
                {
                    "field_id": 1300595,
                    "values": [
                        {
                            "value": user.phone
                        }
                    ]
                },
                {
                    "field_id": 1300597,
                    "values": [
                        {
                            "value": note_type
                        }
                    ]
                }
            ]
        }
    ]
    client.add_elements_to_catalog(
        catalog['id'], elements
    )


def _get_catalog(client: AmoOAuthClient) -> dict:
    catalogs = client.get_catalogs()['_embedded']['catalogs']
    filtered_catalogs = list(filter(lambda catalog: catalog['name'] == 'Клиенты Masspower Bot', catalogs))
    if len(filtered_catalogs) == 0:
        created_catalogs = client.create_catalogs([{
            "name": "Клиенты Masspower Bot",
            "can_add_elements": True,
            "can_link_multiple": False
        }])

        return created_catalogs['_embedded']['catalogs'][0]
    return filtered_catalogs[0]

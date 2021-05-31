import requests
from Conf.conf import SERVICES_URL
from urllib.parse import urljoin
from util.http.methods import ToValidateMethods
from typing import List


def authUser(token: str, request_method: str, avaible_methods: List[str] = ToValidateMethods(), **validate_fields) -> object:
    return requests.post(
            urljoin(SERVICES_URL.AUTH, 'api/v1/auth'),
            json={
                'to_validate': [validate_fields],
                'token': f'{token}',
                'method': {
                    "request_method": request_method,
                    "avaible_methods": avaible_methods.methods
                }
            },
            headers={
                'Authorization': f'jwt {token}'
            }
        )
import requests
from typing import Any
import copy



class Cep(object):
    def __init__(self, value) -> None:
        self.request: Any = f"https://viacep.com.br/ws/{value}/json/"
        self.data: dict
        self.is_valid: bool

    def __str__(self):
        return self.request.text

    def __getitem__(self, key):
        return self.data[key]

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: Any):
        if isinstance(value, requests.models.Response):
            self._data = value.json()
        else:
            self._data = value

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value: str):
        make_request = requests.get(value)
        if make_request.status_code <= 200:
            self._request = make_request
            self.data = self.request
            self.is_valid = True
        else:
            self.is_valid = False
            self.data = dict()

    def map_fields(self, fields: dict) -> object:
        to_return = dict()
        copyed_data = copy.deepcopy(self.data)

        for data_field in self.data:
            for field in fields:
                if data_field == field:
                    to_return.update(
                        {fields[field]: copyed_data[data_field]}
                    )
                    del copyed_data[data_field]
        self.data = to_return
        return self

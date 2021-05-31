from typing import NamedTuple
from collections import namedtuple


class DataBaseConfiguration(NamedTuple):
    NAME: str = "UserDataBase"
    USER: str = "root"
    PASSWORD: str = "rootpassword"
    HOST: str = "172.17.0.1"
    PORT: str = "3306"


DATA_BASE = DataBaseConfiguration()


class ServicesURL(NamedTuple):
    AUTH: str = 'http://172.17.0.1:8080'


SERVICES_URL = ServicesURL()
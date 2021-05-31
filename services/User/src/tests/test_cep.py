import os
import sys
sys.path.insert(0, os.path.abspath('../'))

from cep import Cep
import unittest
from typing import NamedTuple


class TestConfig(NamedTuple):
    correct_cep = '88351001'
    expected_integration_maped_response: dict = {
        'cep': '88351-001',
        'address': 'Rua Felipe Schmidt',
        'complemento': 'de 262 ao fim - lado par',
        'district': 'São Luiz',
        'city': 'Brusque',
        'state': 'SC',
        'ibge': '4202909',
        'gia': '',
        'ddd': '47',
        'siafi': '8055'
    }
    expected_integration_response = {
        'cep': '88351-001',
        'logradouro': 'Rua Felipe Schmidt',
        'complemento': 'de 262 ao fim - lado par',
        'bairro': 'São Luiz',
        'localidade': 'Brusque',
        'uf': 'SC',
        'ibge': '4202909',
        'gia': '',
        'ddd': '47',
        'siafi': '8055'
    }
    incorrect_cep = '0'



class TestCep(unittest.TestCase):
    conf = TestConfig()

    def test_cep(self) -> None:
        cep = Cep(value=self.conf.correct_cep)
        self.assertEqual(
            first=cep.data,
            second=self.conf.expected_integration_response,
            msg="blabalbal"
        )
        
    def test_incorrect_cep(self) -> None:
        with self.assertRaises(ValueError):
            Cep(value=self.conf.incorrect_cep)

    def test_convert_fields(self):
        cep = Cep(value=self.conf.correct_cep)
        cep.map_fields(
            fields={
                'logradouro': 'address', 
                'bairro': 'district',
                'localidade': 'city',
                'uf': 'state'
            }
        )
        self.assertEqual(
            cep.data,
            self.conf.expected_integration_maped_response
        )

    def test_bad_convert_fields(self):
        cep = Cep(value=self.conf.correct_cep)
        cep.map_fields(
            fields={
                'logra*douro': 'address_', 
                'bai-rro': 'district_',
                'localidade': 'city_',
                'uf': 'state'
            }
        )
        self.assertNotEqual(
            cep.data,
            self.conf.expected_integration_maped_response
        )

    def test_valid_cep(self):
        cep = Cep(value=self.conf.correct_cep)
        self.assertTrue(cep.is_valid)

    def test_invalid_cep(self):
        cep = Cep(value=self.conf.incorrect_cep)
        self.assertFalse(cep.is_valid)


if __name__ == "__main__":
    unittest.main()
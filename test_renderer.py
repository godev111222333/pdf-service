import unittest

from unittest import TestCase
from app import app


class TestContractRenderer(TestCase):
    def test_render_customer_contract(self):
        client = app.test_client()
        payload = {'fullName': "Customer", 'dateOfBirth': '9/9/1999', 'year': '2025'}
        response = client.post('/render_customer_contract', json=payload)
        assert 200 == response.status_code
        assert response.json['url'] == 'awss3.com'


if __name__ == '__main__':
    unittest.main()

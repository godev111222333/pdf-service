import unittest

import pytest

from app import Config, app


@pytest.fixture
def app_config():
    return Config("config.yml")


def test_render_customer_contract(app_config):
    client = app.test_client()
    payload = {'fullName': "Customer", 'dateOfBirth': '9/9/1999', 'year': '2025'}
    response = client.post('/render_customer_contract', json=payload)
    assert 200 == response.status_code
    assert len(response.json['uuid']) != 0


if __name__ == '__main__':
    unittest.main()

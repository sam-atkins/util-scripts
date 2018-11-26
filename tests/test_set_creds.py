import json

from src.set_creds import parse_creds_response
from tests.datasets import response


def test_parse_creds_response_returns_values():
    json_response = json.dumps(response.AWS_RESPONSE)
    expected_values = parse_creds_response(json_response)
    assert expected_values == ('response__SecretAccessKey',
                               'response__SessionToken',
                               'response__AccessKeyId')

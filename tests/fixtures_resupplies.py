import pytest


@pytest.fixture(
    params=[
        {
            'request_body': {},
            'response_body': {
                'detail': [
                    {'loc': ['body', 'walletId'], 'msg': 'field required', 'type': 'value_error.missing'},
                    {'loc': ['body', 'amount'], 'msg': 'field required', 'type': 'value_error.missing'}
                ]
            }
        },
        {
            'request_body': {'walletId': 123},
            'response_body': {
                'detail': [
                    {'loc': ['body', 'amount'], 'msg': 'field required', 'type': 'value_error.missing'}
                ]
            }
        },
        {
            'request_body': {'amount': 22},
            'response_body': {
                'detail': [
                    {'loc': ['body', 'walletId'], 'msg': 'field required', 'type': 'value_error.missing'}
                ]
            }
        },
        {
            'request_body': {'walletId': 123, 'amount': None},
            'response_body': {
                'detail': [
                    {
                        'loc': ['body', 'amount'],
                        'msg': 'none is not an allowed value',
                        'type': 'type_error.none.not_allowed'
                    }
                ]
            }
        },
        {
            'request_body': {'walletId': None, 'amount': 22},
            'response_body': {
                'detail': [
                    {
                        'loc': ['body', 'walletId'],
                        'msg': 'none is not an allowed value',
                        'type': 'type_error.none.not_allowed'
                    }
                ]
            }
        },
        {
            'request_body': {'walletId': 123, 'amount': 0},
            'response_body': {
                'detail': [
                    {
                        'loc': ['body', 'amount'],
                        'msg': 'ensure this value is greater than 0',
                        'type': 'value_error.number.not_gt',
                        'ctx': {'limit_value': 0.0}
                    }
                ]
            }
        },
        {
            'request_body': {'walletId': 123, 'amount': -3.23},
            'response_body': {
                'detail': [
                    {
                        'loc': ['body', 'amount'],
                        'msg': 'ensure this value is greater than 0',
                        'type': 'value_error.number.not_gt',
                        'ctx': {'limit_value': 0.0}
                    }
                ]
            }
        },
    ],
    ids=[
        'missed_body',
        'missed_amount',
        'missed_walletId',
        'null_amount',
        'null_walletId',
        'zero_amount',
        'negative_amount',
    ]
)
def create_resupplies_invalid_body(request):
    return request.param


@pytest.fixture(
    params=[
        {
            'request_body': {'walletId': 123, 'amount': 50.34},
            'response_body': {
                'walletId': 123,
                'amount': 50.34,
                'transactionNumber': '39ba4a9b-aa0c-4e81-a134-60271ebb49ed',
                'walletBalance': 76.331
            },
            'mock_data': {
                'wallet_id': 123,
                'amount': 50.34,
                'transaction_number': '39ba4a9b-aa0c-4e81-a134-60271ebb49ed',
                'wallet_balance': 76.331
            },
        },
    ],
    ids=['create_resupply']
)
def create_resupplies_valid_body(request):
    return request.param

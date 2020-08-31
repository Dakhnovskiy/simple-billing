from decimal import Decimal

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


@pytest.fixture(
    params=[
        {
            'request_body': {'walletId': 123, 'amount': 50.34},
            'response_body': {'detail': 'Wallet id 123 not found'}
        },
    ],
    ids=['create_resupply_wallet_not_found']
)
def create_resupplies_wallet_not_found(request):
    return request.param


@pytest.fixture(
    params=[
        {
            'params': {'wallet_id': 123, 'amount': Decimal(50.34)},
            'result': {
                'wallet_id': 123,
                'amount': 50.34,
                'transaction_number': '39ba4a9b-aa0c-4e81-a134-60271ebb49ed',
                'wallet_balance': 76.331
            },
            'generate_transaction_number_mock_data': '39ba4a9b-aa0c-4e81-a134-60271ebb49ed',
            'transaction_create_mock_data': 11,
            'wallet_change_balance_mock_data': Decimal(76.331),
            'wallets_operation_create_mock_data': 5,
            'error_message': 'Wallet id 123 not found',
        },
    ],
    ids=['create_resupply_data']
)
def create_resupply_data(request):
    return request.param

from decimal import Decimal

import pytest


@pytest.fixture(
    params=[
        {
            'request_body': {},
            'response_body': {
                'detail': [
                    {'loc': ['body', 'walletFromId'], 'msg': 'field required', 'type': 'value_error.missing'},
                    {'loc': ['body', 'walletToId'], 'msg': 'field required', 'type': 'value_error.missing'},
                    {'loc': ['body', 'amount'], 'msg': 'field required', 'type': 'value_error.missing'}
                ]
            }
        },
        {
            'request_body': {'walletFromId': 123},
            'response_body': {
                'detail': [
                    {'loc': ['body', 'walletToId'], 'msg': 'field required', 'type': 'value_error.missing'},
                    {'loc': ['body', 'amount'], 'msg': 'field required', 'type': 'value_error.missing'}
                ]
            }
        },
        {
            'request_body': {'walletToId': 22},
            'response_body': {
                'detail': [
                    {'loc': ['body', 'walletFromId'], 'msg': 'field required', 'type': 'value_error.missing'},
                    {'loc': ['body', 'amount'], 'msg': 'field required', 'type': 'value_error.missing'}
                ]
            }
        },
        {
            'request_body': {'amount': 22.2},
            'response_body': {
                'detail': [
                    {'loc': ['body', 'walletFromId'], 'msg': 'field required', 'type': 'value_error.missing'},
                    {'loc': ['body', 'walletToId'], 'msg': 'field required', 'type': 'value_error.missing'}
                ]
            }
        },
        {
            'request_body': {'walletFromId': None, 'walletToId': 123, 'amount': 2.2},
            'response_body': {
                'detail': [
                    {
                        'loc': ['body', 'walletFromId'],
                        'msg': 'none is not an allowed value',
                        'type': 'type_error.none.not_allowed'
                    }
                ]
            }
        },
        {
            'request_body': {'walletFromId': 123, 'walletToId': None, 'amount': 2.2},
            'response_body': {
                'detail': [
                    {
                        'loc': ['body', 'walletToId'],
                        'msg': 'none is not an allowed value',
                        'type': 'type_error.none.not_allowed'
                    }
                ]
            }
        },
        {
            'request_body': {'walletFromId': 123, 'walletToId': 23, 'amount': None},
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
            'request_body': {'walletFromId': 123, 'walletToId': 23, 'amount': 0},
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
            'request_body': {'walletFromId': 123, 'walletToId': 23, 'amount': -123.33},
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
            'request_body': {'walletFromId': 123, 'walletToId': 123, 'amount': 20},
            'response_body': {
                'detail': [
                    {
                        'loc': ['body', '__root__'],
                        'msg': 'wallets must be different',
                        'type': 'value_error'
                    }
                ]
            }
        },
    ],
    ids=[
        'missed_body',
        'only_walletFromId_filled',
        'only_walletToId_filled',
        'only_amount_filled',
        'null_walletFromId',
        'null_walletToId',
        'null_amount',
        'zero_amount',
        'negative_amount',
        'identical wallets',
    ]
)
def create_transfers_invalid_body(request):
    return request.param


@pytest.fixture(
    params=[
        {
            'request_body': {'walletFromId': 123, 'walletToId': 1234, 'amount': 50.34},
            'response_body': {
                'walletFromId': 123,
                'walletToId': 1234,
                'amount': 50.34,
                'transactionNumber': '39ba4a9b-aa0c-4e81-a134-60271ebb49ed',
                'walletFromBalance': 76.331,
                'walletToBalance': 1234.22,
            },
            'mock_data': {
                'wallet_from_id': 123,
                'wallet_to_id': 1234,
                'amount': Decimal(50.34),
                'transaction_number': '39ba4a9b-aa0c-4e81-a134-60271ebb49ed',
                'wallet_from_balance': Decimal(76.331),
                'wallet_to_balance': Decimal(1234.22),
            },
        },
    ],
    ids=['create_transfer']
)
def create_transfers_valid_body(request):
    return request.param


@pytest.fixture(
    params=[
        {
            'request_body': {'walletFromId': 123, 'walletToId': 1234, 'amount': 50.34},
            'response_body': {'detail': 'Wallet id 1234 not found'}
        },
    ],
    ids=['create_transfer_wallet_not_found']
)
def create_transfers_wallet_not_found(request):
    return request.param


@pytest.fixture(
    params=[
        {
            'request_body': {'walletFromId': 123, 'walletToId': 1234, 'amount': 50.34},
            'response_body': {'detail': 'There are not enough balance in wallet id 123'}
        },
    ],
    ids=['create_transfers_not_enough_balance']
)
def create_transfers_not_enough_balance(request):
    return request.param


@pytest.fixture(
    params=[
        {
            'params': {'wallet_from_id': 123, 'wallet_to_id': 1234, 'amount': Decimal(50.34)},
            'result': {
                'wallet_from_id': 123,
                'wallet_to_id': 1234,
                'amount': Decimal(50.34),
                'transaction_number': '39ba4a9b-aa0c-4e81-a134-60271ebb49ed',
                'wallet_from_balance': Decimal(76.331),
                'wallet_to_balance': Decimal(76.331),
            },
            'generate_transaction_number_mock_data': '39ba4a9b-aa0c-4e81-a134-60271ebb49ed',
            'transaction_create_mock_data': 11,
            'wallet_change_balance_mock_data': Decimal(76.331),
            'wallets_operation_create_mock_data': 5,
            'error_message_wallet_not_found': 'Wallet id 1234 not found',
            'error_message_not_enough_balance': 'There are not enough balance in wallet id 123',
        },
    ],
    ids=['create_transfer_data']
)
def create_transfer_data(request):
    return request.param

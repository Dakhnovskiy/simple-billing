import pytest


@pytest.fixture(
    params=[
        {
            'request_body': {},
            'response_body': {
                'detail': [
                    {'loc': ['body', 'login'], 'msg': 'field required', 'type': 'value_error.missing'},
                    {'loc': ['body', 'name'], 'msg': 'field required', 'type': 'value_error.missing'}
                ]
            }
        },
        {
            'request_body': {'name': 'Иванов Иван'},
            'response_body': {
                'detail': [
                    {'loc': ['body', 'login'], 'msg': 'field required', 'type': 'value_error.missing'},
                ]
            }
        },
        {
            'request_body': {'login': 'master'},
            'response_body': {
                'detail': [
                    {'loc': ['body', 'name'], 'msg': 'field required', 'type': 'value_error.missing'},
                ]
            }
        },
        {
            'request_body': {'login': '', 'name': 'Иванов'},
            'response_body': {
                'detail': [
                    {
                        'loc': ['body', 'login'],
                        'msg': 'ensure this value has at least 1 characters',
                        'type': 'value_error.any_str.min_length',
                        'ctx': {'limit_value': 1}
                    }
                ]
            }
        },
        {
            'request_body': {'login': 'myLogin', 'name': ''},
            'response_body': {
                'detail': [
                    {
                        'loc': ['body', 'name'],
                        'msg': 'ensure this value has at least 1 characters',
                        'type': 'value_error.any_str.min_length',
                        'ctx': {'limit_value': 1}
                    }
                ]
            }
        },
        {
            'request_body': {'login': None, 'name': 'Иванов'},
            'response_body': {
                'detail': [
                    {
                        'loc': ['body', 'login'],
                        'msg': 'none is not an allowed value',
                        'type': 'type_error.none.not_allowed'
                    }
                ]
            }
        },
        {
            'request_body': {'login': 'myLogin', 'name': None},
            'response_body': {
                'detail': [
                    {
                        'loc': ['body', 'name'],
                        'msg': 'none is not an allowed value',
                        'type': 'type_error.none.not_allowed'
                    }
                ]
            }
        },
    ],
    ids=['missed_body', 'missed_login', 'missed_name', 'empty_login', 'empty_name', 'null_login', 'null_name']
)
def create_clients_invalid_body(request):
    return request.param


@pytest.fixture(
    params=[
        {
            'request_body': {'login': 'myLogin', 'name': 'Иванов Иван'},
            'response_body': {
                'id': 1593,
                'walletId': 123,
                'login': 'myLogin',
                'name': 'Иванов Иван'
            },
            'mock_data': {
                'id': 1593,
                'wallet_id': 123,
                'login': 'myLogin',
                'name': 'Иванов Иван'
            },
        },
    ],
    ids=['create_client_and_wallet']
)
def create_clients_valid_body(request):
    return request.param


@pytest.fixture(
    params=[
        {
            'request_body': {'login': 'myLogin', 'name': 'Иванов Иван'},
            'response_body': {'detail': 'Client login already exists'},
        },
    ],
    ids=['create_client_already_exists']
)
def create_client_already_exists(request):
    return request.param


@pytest.fixture(
    params=[
        {
            'params': {'login': 'login', 'name': 'Имя Имечко'},
            'result': {
                'id': 111,
                'wallet_id': 222,
                'login': 'login',
                'name': 'Имя Имечко'
            },
            'client_create_mock_data': 111,
            'wallet_create_mock_data': 222,
            'error_message': 'Client login already exists',
        },
    ],
    ids=['create_client_with_wallet_data']
)
def create_client_with_wallet_data(request):
    return request.param

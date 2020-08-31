class BillingOperationException(Exception):
    def __init__(self, message: str, *args):
        super().__init__(*args)
        self.message = message


class ClientLoginAlreadyExists(BillingOperationException):
    ERROR_MESSAGE = 'Client login already exists'

    def __init__(self, *args):
        super().__init__(self.ERROR_MESSAGE, *args)


class WalletExceptions(BillingOperationException):
    ERROR_MESSAGE: str

    def __init__(self, wallet_id: int, *args):
        super().__init__(self.ERROR_MESSAGE.format(wallet_id=wallet_id), *args)


class WalletNotFound(WalletExceptions):
    ERROR_MESSAGE = 'Wallet id {wallet_id} not found'


class NotEnoughBalance(WalletExceptions):
    ERROR_MESSAGE = 'There are not enough balance in wallet id {wallet_id}'

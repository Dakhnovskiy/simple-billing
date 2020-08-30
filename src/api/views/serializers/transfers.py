from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, condecimal, root_validator


class TransferCreateBase(BaseModel):
    wallet_from_id: int = Field(alias='walletFromId')
    wallet_to_id: int = Field(alias='walletToId')
    amount: condecimal(gt=Decimal(0))

    class Config:
        allow_population_by_field_name = True


class TransferCreateRequest(TransferCreateBase):

    @root_validator
    def check_wallets_identifiers(cls, values):
        if values.get('wallet_from_id') is None or values.get('wallet_to_id') is None:
            return values

        if values.get('wallet_from_id') == values.get('wallet_to_id'):
            raise ValueError('wallets must be different')

        return values


class TransferCreateResponse(TransferCreateBase):
    transaction_number: UUID = Field(alias='transactionNumber')
    wallet_from_balance: condecimal() = Field(alias='walletFromBalance')
    wallet_to_balance: condecimal() = Field(alias='walletToBalance')

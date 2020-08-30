from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, condecimal


class TransferCreateBase(BaseModel):
    wallet_from_id: int = Field(alias='walletFromId')
    wallet_to_id: int = Field(alias='walletToId')
    amount: condecimal(gt=Decimal(0))

    class Config:
        allow_population_by_field_name = True


class TransferCreateRequest(TransferCreateBase):
    pass


class TransferCreateResponse(TransferCreateBase):
    transaction_number: UUID = Field(alias='transactionNumber')
    wallet_from_balance: condecimal() = Field(alias='walletFromBalance')
    wallet_to_balance: condecimal() = Field(alias='walletToBalance')

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class TransferCreateBase(BaseModel):
    wallet_id_from: int = Field(alias='walletIdFrom')
    wallet_id_to: int = Field(alias='walletIdTo')
    amount: Decimal = Field(gt=0)

    class Config:
        allow_population_by_field_name = True


class TransferCreateRequest(TransferCreateBase):
    pass


class TransferCreateResponse(TransferCreateBase):
    transaction_number: UUID = Field(alias='transactionNumber')
    wallet_balance_from: Decimal() = Field(alias='walletBalanceFrom')
    wallet_balance_to: Decimal() = Field(alias='walletBalanceTo')

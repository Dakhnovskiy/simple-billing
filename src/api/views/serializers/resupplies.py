from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class ResupplyCreateBase(BaseModel):
    wallet_id: int = Field(alias='walletId')
    amount: Decimal = Field(gt=0)

    class Config:
        allow_population_by_field_name = True


class ResupplyCreateRequest(ResupplyCreateBase):
    pass


class ResupplyCreateResponse(ResupplyCreateBase):
    transaction_number: UUID = Field(alias='transactionNumber')
    wallet_balance: Decimal() = Field(alias='walletBalance')


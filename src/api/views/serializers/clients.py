from pydantic import BaseModel, Field


class ClientBase(BaseModel):
    login: str = Field(min_length=1, max_length=256)
    name: str = Field(min_length=1, max_length=256)


class ClientCreateRequest(ClientBase):
    pass


class ClientCreateResponse(ClientBase):
    id: int
    wallet_id: int = Field(alias='walletId')
    
    class Config:
        allow_population_by_field_name = True



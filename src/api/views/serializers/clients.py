from pydantic import BaseModel, Field


class ClientBase(BaseModel):
    login: str = Field(min_length=1, max_length=256)
    name: str = Field(min_length=1, max_length=256)


class ClientCreate(ClientBase):
    pass


class ClientInfo(ClientBase):
    id: int
    wallet_id: int


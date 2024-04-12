from pydantic import BaseModel


class UpdateAddress(BaseModel):
    new_address: str
    old_address: str


class AddressDetails(BaseModel):
    address: str
    latitude: float
    longitude: float


class AddAddress(BaseModel):
    address: str

from pydantic import BaseModel, Json
from typing import Optional


class CityCreate(BaseModel):
    id: int
    city_name: str

    class Config:
        orm_mode = True


class Payload(BaseModel):
    id: int
    temperature: int
    wind: float
    pressure: int

    class Config:
        orm_mode = True

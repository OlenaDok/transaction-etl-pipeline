from datetime import date
from decimal import Decimal

from pydantic import BaseModel, computed_field


class Rate(BaseModel):
    rate_date: date
    currency_code: str
    currency_name: str | None
    nominal: int
    rate: Decimal

    @computed_field
    @property
    def rate_per_unit(self) -> Decimal:
        return round(self.rate / self.nominal, 6)


class Health(BaseModel):
    status: str
    message: str
    temperature: float

    @computed_field
    @property
    def check_temperature(self) -> str:
        if self.temperature > 37.0:
            return "you need to rest. you sick now"
        return "you fine! let`s work and code!"

from pydantic import BaseModel


class Currency(BaseModel):
    amount: int = 1
    from_currency: str = "USD"
    to_currency: str = "RUB"

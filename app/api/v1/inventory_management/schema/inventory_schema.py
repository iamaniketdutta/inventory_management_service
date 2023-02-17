from typing import List, Optional

from configuration.constants import Numeric
from pydantic import BaseModel, Field
from pydantic.types import StrictBool, StrictInt


class GetQueryModel(BaseModel):
    page_number: Optional[int] = Field(ge=Numeric.ONE.value, default=Numeric.ONE.value)
    page_limit: Optional[int] = Field(
        ge=Numeric.ONE.value, default=Numeric.TWENTY.value
    )
    order_by: Optional[str]


class InventoryGetResp(BaseModel):
    brand: str
    additionalInfo: str
    original_price: float
    discounted_price: float
    discount_percentage: int
    rating: float
    review_count: str
    out_of_stock: StrictBool


class GetInventoryResponse(BaseModel):
    count: StrictInt = Numeric.ZERO.value
    items: List[InventoryGetResp] = []


class SuccessResponseGet(BaseModel):
    data: Optional[GetInventoryResponse] = {}
    success: StrictBool = True

from typing import Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float
    discounted_price: Optional[float] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    model_config = {
        "from_attributes": True
    }
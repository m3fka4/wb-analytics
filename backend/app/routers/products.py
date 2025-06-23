from typing import List, Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/api/products", tags=["products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.Product])
def read_products(
    min_price: float = Query(0.0, ge=0.0),
    max_price: Optional[float] = Query(None, ge=0.0),
    min_rating: float = Query(0.0, ge=0.0, le=5.0),
    min_reviews: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """
    Retrieve products with optional filtering:
    - min_price: float (>= 0)
    - max_price: float (>= 0)
    - min_rating: float between 0 and 5
    - min_reviews: int (>= 0)
    """
    try:
        products = crud.get_products(
            db,
            min_price=min_price,
            max_price=max_price,
            min_rating=min_rating,
            min_reviews=min_reviews,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch products")
    return products
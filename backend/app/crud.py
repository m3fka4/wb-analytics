from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas

def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:

    db_item = models.Product(**product.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_products(
    db: Session,
    min_price: float = 0.0,
    max_price: Optional[float] = None,
    min_rating: float = 0.0,
    min_reviews: int = 0,
) -> List[models.Product]:

    query = db.query(models.Product).filter(
        models.Product.price >= min_price,
        models.Product.rating >= min_rating,
        models.Product.reviews_count >= min_reviews,
    )
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    return query.all()
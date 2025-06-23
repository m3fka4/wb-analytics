from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    discounted_price = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, nullable=True)

    def __repr__(self):
        return (
            f"<Product(id={self.id!r}, name={self.name!r}, price={self.price!r}, "
            f"discounted_price={self.discounted_price!r}, rating={self.rating!r}, "
            f"reviews_count={self.reviews_count!r})>"
        )
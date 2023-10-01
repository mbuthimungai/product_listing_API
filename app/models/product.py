from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .base import Base_

class Product(Base_):
    """
    This is the SQLAlchemy class for defining the product model.
    It inherits all the attributes and methods of Base_ class.
    This class defines common attributes such as name, price image,
    and weight.
    Attributes:
        name (str): The product name
        price (str): The product price
        image (str): The product image url
        weight (str): The product price
    'nullable=False' means these columns cannot have NULL values in the database.
    """
    name: Mapped[str] = mapped_column(String(30), index=True, nullable=False)
    price: Mapped[str] = mapped_column(String(30), nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=False)
    weight: Mapped[str] = mapped_column(String, nullable=False)
    
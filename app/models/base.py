from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, declared_attr, DeclarativeBase, mapped_column
from app.utils.idgen import idgen
from datetime import datetime


class Base_(DeclarativeBase):
    """
    Base class for SQLAlchemy models with common attributes to stay DRY (Don't Repeat Yourself).

    This class is intended to serve as a base class for SQLAlchemy models.
    It defines common attributes such as table name, creation timestamp,
    and update timestamp that can be inherited by other models, helping you
    to adhere to the DRY (Don't Repeat Yourself) principle.

    Attributes:
        __tablename__ (str): The table name, derived from the class name in lowercase.
        id (str): The unique ID of each record.
        created_on (datetime): The timestamp of when the record was created.
        updated_on (datetime, optional): The timestamp of when the record was last updated.
            Defaults to None until an update occurs.

    Example:
        To create a SQLAlchemy model using this base class:

        ```python
        class YourModel(Base_):
            # Define additional attributes for your model here.
        ```

    """
    @declared_attr
    def __tablename__(cls):
        # The table name is derived from the class name in lowercase
        return cls.__name__.lower()
    
    # The unique UUID ID for each record
    id: Mapped[str] = mapped_column(primary_key=True, default=idgen,index=True)
    
    # The timestamp for record creation
    created_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # The timestamp for record update, initially None until an update occurs
    updated_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
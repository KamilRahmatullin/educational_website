from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .product import Product
    from .order_product_association import OrderProductAssociation


class Order(Base):
    promocode: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now()
    )

    # Define a relationship with the OrderProductAssociation class through order
    products_details: Mapped[list["OrderProductAssociation"]] = relationship(back_populates="order")

    def __str__(self):
        return f"{self.__class__.__name__} {self.id} {self.created_at}"

    def __repr__(self):
        return str(self)

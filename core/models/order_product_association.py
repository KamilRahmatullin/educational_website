from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .order import Order
    from .product import Product


# Define the OrderProductAssociation class that represents the association between orders and products
class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    # Define a unique constraint on the combination of order_id and product_id
    __table_args__ = (
        UniqueConstraint(
            'order_id', 'product_id', name='idx_unique_order_product'
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    count: Mapped[int] = mapped_column(default=1, server_default="1")

    # Define the relationship between the OrderProductAssociation and the Order class.
    order: Mapped["Order"] = relationship(back_populates="products_details")
    # Define the relationship between the OrderProductAssociation and the Product class.
    product: Mapped["Product"] = relationship(back_populates="orders_details")

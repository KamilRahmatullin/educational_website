from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class User(Base):
    name: Mapped[str] = mapped_column(String(32), unique=True)
    description: Mapped[str]
    price: Mapped[int]
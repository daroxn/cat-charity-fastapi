from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin


class InvestmentMixin(CommonMixin, Base):
    """Базовая модель с общими полями для инвестируемых объектов."""

    __abstract__ = True

    full_amount: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint('full_amount > 0'),
        nullable=False
    )
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint('invested_amount >= 0'),
        default=0,
        nullable=False
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    close_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

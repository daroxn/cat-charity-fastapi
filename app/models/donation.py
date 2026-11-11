from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import InvestmentMixin


class Donation(InvestmentMixin):
    """Модель пожертвования."""

    comment: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id', name='fk_reservation_user_id_user'),
        nullable=True
    )

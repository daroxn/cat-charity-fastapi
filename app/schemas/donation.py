from datetime import datetime

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DonationBase(BaseModel):
    """Базовая схема пожертвования с обязательным полем суммы."""

    full_amount: int = Field(
        ...,
        gt=0
    )

    model_config = ConfigDict(extra='forbid')


class DonationCreate(DonationBase):
    """Схема для создания нового пожертвования."""

    comment: Optional[str] = None


class DonationDB(DonationBase):
    """Схема пожертвования с базовыми данными из базы данных."""

    id: int
    comment: Optional[str]
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationDB):
    """Схема пожертвования с полными данными, включая статус инвестирования."""

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

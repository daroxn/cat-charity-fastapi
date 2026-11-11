from datetime import datetime

from typing import Optional

from pydantic import (
    BaseModel, ConfigDict, Field
)


class CharityProjectBase(BaseModel):
    """Базовая схема благотворительного проекта с обязательными полями."""

    name: str = Field(
        ...,
        min_length=5,
        max_length=100
    )
    description: str = Field(
        ...,
        min_length=10
    )
    full_amount: int = Field(
        ...,
        gt=0
    )

    model_config = ConfigDict(extra='forbid')


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания нового благотворительного проекта."""


class CharityProjectUpdate(BaseModel):
    """Схема для частичного обновления благотворительного проекта."""

    name: Optional[str] = Field(
        None,
        min_length=5,
        max_length=100
    )
    description: Optional[str] = Field(
        None,
        min_length=10
    )
    full_amount: Optional[int] = Field(
        None,
        gt=0
    )

    model_config = ConfigDict(extra='forbid')


class CharityProjectDB(CharityProjectBase):
    """Схема проекта с полными данными из базы данных."""

    id: int
    invested_amount: int
    full_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

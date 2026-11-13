from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Базовая схема пользователя."""


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания нового пользователя."""


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления данных пользователя."""

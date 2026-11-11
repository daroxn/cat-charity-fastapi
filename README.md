# QRKot — Благотворительный фонд поддержки котиков

REST API для управления благотворительными проектами и пожертвованиями фонда QRKot.

---

## Стек технологий

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic v2
- aiosqlite
- Uvicorn

## Установка и запуск

```bash
# Клонировать репозиторий
git clone <repo-url>
cd cat-charity-1

# Создать и активировать виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Установить зависимости
pip install -r requirements.txt

# Создать .env файл
echo "DATABASE_URL=sqlite+aiosqlite:///./fastapi.db" > .env

# Применить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload
```

Документация API доступна по адресу:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## Структура проекта

```
app/
├── api/
│   ├── endpoints/
│   │   ├── charity_project.py   # Эндпоинты целевых проектов
│   │   └── donation.py          # Эндпоинты пожертвований
│   ├── routers.py               # Главный роутер
│   └── validators.py            # Валидаторы бизнес-логики
├── core/
│   ├── config.py                # Настройки приложения (pydantic-settings)
│   └── db.py                    # Подключение к БД, Base, CommonMixin
├── crud/
│   ├── base.py                  # Базовый CRUD (get, get_all, create, update, remove)
│   ├── charity_project.py       # CRUD для CharityProject
│   └── donation.py              # CRUD для Donation
├── models/
│   ├── charity_project.py       # ORM-модель CharityProject
│   └── donation.py              # ORM-модель Donation
├── schemas/
│   ├── charity_project.py       # Pydantic-схемы для проектов
│   └── donation.py              # Pydantic-схемы для пожертвований
├── services/
│   └── investsments.py          # Логика инвестирования пожертвований
└── main.py                      # Точка входа FastAPI
```

---

## ORM-модели

### CharityProject (таблица `charityproject`)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer, PK | Первичный ключ |
| `name` | String(100), unique | Уникальное название проекта (5–100 символов) |
| `description` | String | Описание проекта (не менее 10 символов) |
| `full_amount` | Integer | Целевая сумма сбора (> 0) |
| `invested_amount` | Integer | Собрано на текущий момент (default: 0) |
| `fully_invested` | Boolean | Флаг закрытия проекта (default: False) |
| `create_date` | DateTime | Дата создания (заполняется автоматически) |
| `close_date` | DateTime, nullable | Дата закрытия (заполняется автоматически) |

### Donation (таблица `donation`)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer, PK | Первичный ключ |
| `comment` | String, nullable | Комментарий к пожертвованию |
| `full_amount` | Integer | Сумма пожертвования (> 0) |
| `invested_amount` | Integer | Распределено по проектам (default: 0) |
| `fully_invested` | Boolean | Флаг полного распределения (default: False) |
| `create_date` | DateTime | Дата пожертвования (заполняется автоматически) |
| `close_date` | DateTime, nullable | Дата полного распределения (заполняется автоматически) |

---

## API-эндпоинты

### Целевые проекты `/charity_project/`

| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/charity_project/` | Список всех проектов |
| `POST` | `/charity_project/` | Создать новый проект |
| `PATCH` | `/charity_project/{project_id}` | Обновить проект |
| `DELETE` | `/charity_project/{project_id}` | Удалить проект |

#### POST `/charity_project/` — создание проекта

**Тело запроса:**
```json
{
  "name": "Котики в Москве",
  "description": "Помогаем котикам найти дом",
  "full_amount": 100000
}
```

**Ответ:**
```json
{
  "id": 1,
  "name": "Котики в Москве",
  "description": "Помогаем котикам найти дом",
  "full_amount": 100000,
  "invested_amount": 0,
  "fully_invested": false,
  "create_date": "2024-01-01T10:00:00"
}
```

Поля `invested_amount`, `fully_invested`, `id` — заполняются автоматически.
Сразу после создания запускается процесс инвестирования.

#### PATCH `/charity_project/{project_id}` — обновление проекта

Все поля опциональны. Ограничения:
- Нельзя изменять закрытый проект
- Нельзя устанавливать `full_amount` меньше уже внесённой суммы
- Если `full_amount` установлен равным `invested_amount` — проект автоматически закрывается

#### DELETE `/charity_project/{project_id}` — удаление проекта

- Нельзя удалять проект, в который уже внесены средства
- Нельзя удалять закрытые проекты

---

### Пожертвования `/donation/`

| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/donation/` | Список всех пожертвований (с полной информацией) |
| `POST` | `/donation/` | Создать пожертвование |

#### POST `/donation/` — создание пожертвования

**Тело запроса:**
```json
{
  "full_amount": 5000,
  "comment": "На корм котикам"
}
```

**Ответ (краткая форма):**
```json
{
  "id": 1,
  "full_amount": 5000,
  "comment": "На корм котикам",
  "create_date": "2024-01-01T10:00:00"
}
```

Сразу после создания запускается процесс инвестирования.

#### GET `/donation/` — список пожертвований (полная форма)

```json
[
  {
    "id": 1,
    "full_amount": 5000,
    "comment": "На корм котикам",
    "invested_amount": 5000,
    "fully_invested": true,
    "create_date": "2024-01-01T10:00:00",
    "close_date": "2024-01-01T10:00:01"
  }
]
```

---

## Логика инвестирования

При создании нового проекта или нового пожертвования автоматически запускается
процесс инвестирования (`app/services/investsments.py`):

1. Берутся все **открытые** проекты (у которых `close_date` не задан), отсортированные по `create_date`.
2. Берутся все **неинвестированные** пожертвования (у которых `close_date` не задан), отсортированные по `create_date`.
3. Средства из пожертвований последовательно распределяются в проекты — от самого старого к новому.
4. Если пожертвование покрывает проект полностью — проект закрывается (`fully_invested=True`, проставляется `close_date`).
5. Если все средства пожертвования распределены — пожертвование закрывается аналогично.
6. Всё выполняется в **одной транзакции** (`session.commit()` вызывается один раз в конце).

Вспомогательная функция `close_if_fully_invested(obj)` также используется при
PATCH-обновлении проекта — если после изменения `full_amount == invested_amount`,
проект автоматически закрывается.

---

## Валидация

| Правило | Поле | Описание |
|---------|------|----------|
| `5 ≤ len ≤ 100` | `name` | Длина названия проекта |
| `len ≥ 10` | `description` | Минимальная длина описания |
| `> 0` | `full_amount` | Целевая сумма |
| `> 0` | `full_amount` (donation) | Сумма пожертвования |
| Уникальность | `name` | Имена проектов должны быть уникальными |
| `full_amount ≥ invested_amount` | PATCH проект | Нельзя уменьшить сумму ниже уже вложенной |

---

## Переменные окружения (`.env`)

| Переменная | Описание | Пример |
|------------|----------|--------|
| `DATABASE_URL` | URL базы данных | `sqlite+aiosqlite:///./fastapi.db` |

---

## Миграции (Alembic)

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "описание"

# Применить миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1
```

---

## Тесты

```bash
# Запустить все тесты
pytest tests/ -v

# Запустить с отображением покрытия
pytest tests/ --tb=short
```

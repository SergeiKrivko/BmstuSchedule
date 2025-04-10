# Bmstu Schedule API

## Структура проекта
https://dev.to/mohammad222pr/structuring-a-fastapi-project-best-practices-53l6

## Локальный запуск

## Зависимости

Установка:
```bash
make install
```

Добавление:
1. Добавить зависимость в `pyproject.toml` (poetry или poetry dev, если только для разработки)
2. Зафиксировать
```bash
poetry lock
```
3. Установить
```bash
make install
```

## Локальный запуск

Окружение:
```bash
make run-environment
```

Запуск API:
```bash
make run-api
```

## Тесты/форматтеры/линтеры

Прогнать все сразу (с фиксом проблем):
```bash
make check
```

Прогнать линтеры:
```bash
make lint
```

Прогнать форматтеры:
```bash
make format
```

Прогнать тесты:
```bash
make test
```

## Документация

Сваггер доступен по адресу:
```bash
http://localhost:8000/docs
```

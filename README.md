# Test task app for Dimatech Ltd.
https://docs.google.com/document/d/1-fvs0LaX2oWPjO6w6Bpglz1Ndy_KrNV7NeNgRlks94k/edit?tab=t.0

## Развёртывание локально
Все команды необходимо выполнять в **корневом каталоге проекта**

1. Установка [Docker](https://www.docker.com/get-started/)
2. Скопировать и настроить переменные окружения в файле .env
    ```bash
     copy .env.example .env
    ```
3. Запуск проекта (доступно по адресу https://0.0.0.0:8000)
    ```bash
    docker compose up -d
    ```
4. Остановка проекта и удаление контейнеров и базы данных
    ```bash
    docker compose down -v
    ```
## Прежде чем запустить проект

### Переменные окружения. Файл .env
Для нормальной работы проекта нужно дополнить .env.

## Документация

Документация Swagger API доступна по адресу: http://localhost:8000/api/docs
Документация ReDoc доступна по адресу: http://localhost:8000/api/redoc

## Credentials
При первом запуске приложения alembic автоматически создаст 2х пользователей(простой и с правами администратора).

Простой пользователь:
email - `user@example.com`
password - `usersecretstring`

Администратор:
email - `admin@example.com`
password - `adminsecretstring`
    
## Чистота кода и линтинг
Чистота кода обеспечивается использованием `task` (конфигурация команд в `Taskfile.yml`), но даже если он не установлен, то команды следующие:
```bash
ruff format .  # Автоформатирование под PEP8
ruff check .   # Проверка на наличие неисправленных ошибок
isort .        # Исправление порядка и вида импортов
mypy .         # Проверка аннотаций типов
```

Для запуска локально необходимо настроить подключение к PostgreSQL, либо запусить контейнер `database` используя команду:
```bash
docker compose up -d database
```
предварительно установив значение `DATABASE_HOST=localhost`.

Также, если необходим Debug, следует настроить конфигурацию debug-сервера.

Для vscode:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.app:create_app",
                "--host", "127.0.0.1",
                "--port", "8000",
                "--reload"
            ],
            "jinja": true
        }
    ]
}
```
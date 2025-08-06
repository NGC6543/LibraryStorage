# Описание проекта
Сервис для хранения данных о книгах. Поддерживаются все операции CRUD. Поля книги содержат: название, цену, дату добавления и список авторов. В планах реализовать фронтенд и подключить ML модели.


# Запуск проекта с помощью Docker compose:

Клонировать репозиторий и перейти в него в терминале:
```bash
git clone https://github.com/NGC6543/LibraryStorage.git
```

Создать файл .env и указать данные:
```bash
POSTGRES_DB="LibraryStorage"
DB_HOST=db
POSTGRES_USER=<ваш логин (обычно postgres)>
POSTGRES_PASSWORD=<ваш пароль>
DB_PORT=5432
```

Перейти в директорию infra:
```bash
cd infra/
```

Запустить образы из файла Docker-compose:
```bash
docker compose -f docker-compose.yml up -d --build
```


# Запуск проекта локально:
Клонировать репозиторий и перейти в него в терминале:
```bash 
git clone https://github.com/NGC6543/LibraryStorage.git
```

Установить виртуальное окружение и установить зависимости
```bash
python -m venv venv
pip install -r requirements.txt
```

Установить PostgreSQL и запустить его
```bash
https://www.postgresql.org/download/
```

Создать файл .env и указать данные:
```bash
POSTGRES_DB="LibraryStorage"
DB_HOST=localhost
POSTGRES_USER=<ваш логин (обычно postgres)>
POSTGRES_PASSWORD=<ваш пароль>
DB_PORT=5432
```

Запустить скрипт для создания бд и запуска сервера:
```bash
./run_dev.sh
```

# Стек технологий
- Python 3.11.0
- FastApi
- PostgreSQL
- Docker


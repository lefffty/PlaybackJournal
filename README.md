# PlaybackJournal

## Настройка PostgreSQL для проекта

### Установка локального сервера Postgres

https://www.postgresql.org/download/ - ссылка для установки локального сервера Postgres. Выберите нужную Вам ОС и установите сервер.

После завершения процесса установки перейдите в интерфейс PostgreSQL через терминал с помощью следующей команды:
```
psql
```

Далее, находясь внутри интерфейса PostgreSQL выполните команды ниже:
1. CREATE USER **albums** WITH PASSWORD '**albums**';
2. CREATE DATABASE **albums** OWNER **albums** ENCODING 'UTF8';

Вместо выделенных жирным наименований вы можете придумать и использовать свои.

Создайте в корневой директории проекта файл с расширением "**.env**". В нем укажите следующие значения параметров:
```
DJANGO_SECRET_KEY = 'django-insecure-y9m_py($cd(v8r@cce%+o=ifvz3k&^8yex!(4klf$=7@dm7#*a'
POSTGRES_DB = 'albums'
POSTGRES_USER = 'albums'
POSTGRES_PASSWORD = 'albums'
DB_HOST = 'localhost'
DB_PORT = '5432'
```

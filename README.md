# Django Tracker

### Требования
- Docker
- Docker Compose

### Запуск проекта
1. **Клонируйте репозиторий и перейдите в папку проекта:**
    ```
   git clone https://github.com/your-repository/tracker.git
   cd tracker
    ```

2. **Создайте файл .env с переменными окружения:**
```
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydatabase
```

3. **Запустите контейнеры:**
```docker-compose up -d --build```

4. **Остановка контейнеров**
```docker-compose down```
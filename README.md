# Django Tracker

### Требования
- Docker
- Docker Compose
- GitHub Actions
- SSH доступ к серверу для деплоя

### Описание
Проект Django Tracker использует Docker и Docker Compose для локального и удаленного развертывания. В проекте используется PostgreSQL, Redis, Celery, и Nginx. Для автоматизации деплоя настроен процесс CI/CD с использованием GitHub Actions.

### Запуск проекта
Сервер 84.201.168.17

#### Локальный запуск
1. **Клонируйте репозиторий и перейдите в папку проекта:**
    ```bash
    git clone https://github.com/DRF_Tracker/tracker.git
    cd tracker
    ```

2. **Создайте файл .env с переменными окружения:**
    ```env
    POSTGRES_USER=myuser
    POSTGRES_PASSWORD=mypassword
    POSTGRES_DB=mydatabase
    SECRET_KEY=your-secret-key
    DEBUG=True
    ```

3. **Запустите контейнеры:**
    ```bash
    docker-compose up -d --build
    ```

4. **Остановка контейнеров:**
    ```bash
    docker-compose down
    ```

#### Удаленный запуск через GitHub Actions
Процесс деплоя настроен с использованием GitHub Actions для автоматического разворачивания проекта на удаленном сервере.

1. **Настройка секретов в GitHub:**
    - В разделе `Settings` вашего репозитория, выберите `Secrets and variables` → `Actions` → `New repository secret`.
    - Добавьте следующие секреты:
      - `SSH_KEY` — ваш приватный SSH-ключ для доступа к серверу.
      - `SERVER_IP` — IP-адрес вашего удаленного сервера.
      - `SSH_USER` — пользователь для подключения через SSH.
      - `DEPLOY_DIR` — путь на сервере для размещения проекта.
      - `DJANGO_SECRET_KEY`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `BOT_TOKEN`, `HOST`, `PORT` — другие переменные окружения для Django.

2. **Процесс деплоя через GitHub Actions:**
    - Когда код будет пушен в ветку `develop`, GitHub Actions автоматически выполнит деплой на сервер.
    - В процессе деплоя GitHub Actions выполнит следующие шаги:
        - Клонирование кода на сервер.
        - Установка Docker и Docker Compose на сервер (если они не установлены).
        - Копирование файла `.env` и конфигурации проекта на сервер.
        - Запуск контейнеров через `docker-compose`.
        - Выполнение миграций базы данных.

3. **Описание шагов деплоя в GitHub Actions:**
    ```yaml
    deploy:
      runs-on: ubuntu-latest
      needs: test
      steps:
        - name: Check out code
          uses: actions/checkout@v3

        - name: Set up SSH
          uses: webfactory/ssh-agent@v0.9.0
          with:
            ssh-private-key: ${{ secrets.SSH_KEY }}

        - name: Add server to known_hosts
          run: |
            ssh-keyscan -H ${{ secrets.SERVER_IP }} >> ~/.ssh/known_hosts

        - name: Generate .env file
          run: |
            echo "SECRET_KEY=${{ secrets.DJANGO_SECRET_KEY }}" > .env
            echo "DEBUG=False" >> .env
            echo "POSTGRES_DB=${{ secrets.POSTGRES_DB }}" >> .env
            echo "POSTGRES_USER=${{ secrets.POSTGRES_USER }}" >> .env
            echo "POSTGRES_PASSWORD=${{ secrets.PASSWORD }}" >> .env
            echo "HOST=${{ secrets.HOST }}" >> .env
            echo "PORT=${{ secrets.PORT }}" >> .env
            echo "BOT_TOKEN=${{ secrets.BOT_TOKEN }}" >> .env
            cat .env

        - name: Copy project files to server
          run: |
            rsync -avz --exclude '__pycache__' --exclude 'venv' --exclude '.git' . \
              ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }}:${{ secrets.DEPLOY_DIR }}

        - name: Upload .env to server
          run: |
            rsync -avz .env ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }}:${{ secrets.DEPLOY_DIR }}/.env

        - name: Install Docker and Docker Compose on server (if not installed)
          run: |
            ssh -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} << 'EOF'
              set -e
              if ! command -v docker &> /dev/null; then
                echo "Docker not found. Installing..."
                curl -fsSL https://get.docker.com | sudo sh
                sudo usermod -aG docker $USER
                newgrp docker
              else
                echo "Docker already installed."
              fi

              if ! command -v docker-compose &> /dev/null; then
                echo "Installing Docker Compose..."
                sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                sudo chmod +x /usr/local/bin/docker-compose
              else
                echo "Docker Compose already installed."
              fi
            EOF

        - name: Wait for backend container to be ready
          run: |
            ssh -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} << 'EOF'
              set -e
              until curl -s http://${{ secrets.SERVER_IP }}:8000; do
                echo "Waiting for backend to be ready..."
                sleep 5
              done
              echo "Backend is ready."
            EOF

        - name: Restart docker-compose on server
          run: |
            ssh -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} << 'EOF'
              set -e
              cd ${{ secrets.DEPLOY_DIR }}
              echo "Stopping containers..."
              docker-compose down || { echo "docker-compose down failed"; exit 1; }

              echo "Pulling latest images..."
              docker-compose pull || { echo "docker-compose pull failed"; exit 1; }

              echo "Rebuilding and restarting containers..."
              docker-compose up -d --build || { echo "docker-compose up failed"; exit 1; }

              echo "Docker Compose successfully restarted."
            EOF

        - name: Run database migrations
          run: |
            ssh -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} << 'EOF'
              set -e
              cd ${{ secrets.DEPLOY_DIR }}
              echo "Running database migrations..."
              docker-compose exec backend python manage.py migrate || { echo "Migrations failed"; exit 1; }
            EOF

        - name: Show Postgres logs if failed
          if: failure()
          run: |
            ssh -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} "docker logs postgres_data || true"

        - name: Check running containers
          run: |
            ssh -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} "docker ps"
    ```

### Адрес сервера
Убедитесь, что в репозитории указан правильный IP-адрес вашего сервера, и что вы имеете доступ для деплоя через SSH.

---

Теперь, когда вы запустите изменения в ветке `develop`, GitHub Actions выполнит деплой на сервер, настроив все необходимые шаги.
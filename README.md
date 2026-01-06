# Habits API

API посвящена книге «Атомные привычки» Джеймса Клира о приобретении новых полезных привычек и искоренению старых
плохих. Это backend-трекер полезных привычек.

Для получения документации по API использовать /swagger/ или /redoc/. 

## Домашнее задание: Курс 9. Итоговое задание

## Доступ к API (текущий рабочий сервер)
- API: http://158.160.204.163/
- Документация: http://158.160.204.163/swagger/ или http://158.160.204.163/redoc/
- Админка: http://158.160.204.163/admin/ (Суперпользователь: admin@habi.com  Пароль: 123qwe)

### Локальный запуск

1. Клонируйте репозиторий
2. Создайте файл `.env` по примеру `.env.example`
3. Запустите проект:
`docker-compose up --build`
4. Создайте суперпользователя:  
`docker-compose exec web python manage.py createadmin`
5. Сервис доступен по адресу `http://127.0.0.1`

### Настройка сервера
1. Создайте Ваш сервер на базе Ubuntu, поддерживающем SSH протокол
2. Подключитесь к серверу командой в терминале  
`ssh <user_name>@<your_server_ip>`
3. Выполните обновления ПО на сервере по необходимости  
`sudo apt update && sudo apt upgrade`
4. Выполните настройку фаервола, оставив открытыми только порты 22, 80, 443
```commandline
sudo ufw status  
sudo ufw enable  # Если фаервол отключен
sudo ufw allow 80/tcp  
sudo ufw allow 443/tcp  
sudo ufw allow 22/tcp  
```

### Деплой на сервер
## Первый деплой (выполняется вручную):
1. Создайте директорию где будет храниться проект командой `mkdir <directory>`
2. Перейдите в неё командой `cd <directory>`
3. Настройте сервер с Docker по инструкции
https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
4. Установите docker compose и pip:
```commandline
sudo apt update
sudo apt install docker-compose
sudo apt install git
sudo apt upgrade
```
5. Склонируйте проект на сервер
`git clone -b develop --single-branch https://github.com/AleksandrG-dot/habits_api.git`
6. Создайте .env файл по примеру `.env.example` на сервере в корне проекта командой 'nano .env'
7. Запустите сервер (дождитесь запуска). Затраченное время около 1-5 минут в зависимости от скорости интернет вашего сервера:  
`docker-compose up --build -d`
8. Проверить запуск всех контейнеров:  
`docker ps -a`
9. Создайте суперпользователя:  
`docker-compose exec habits_api python manage.py createadmin`
10. Проект настроен. Поздравляем с успешной настройкой.

## Автоматический деплой через CI/CD (выполнять после первого):
- Условия срабатывания: при push или pull request автоматически запускаются тесты
- При успешных тестах проект деплоится на сервер через DockerHub
- Настройте секреты в GitHub: SSH_KEY, SSH_USER, SERVER_IP, DOCKER_HUB_USERNAME, DOCKER_HUB_ACCESS_TOKEN
- Убедитесь в присутствии файла .env в корне сервера

Создание суперпользователя (при запуске через `python manage.py runserver`):
`python manage.py createadmin`
# yamdb_final

![status workflow](https://github.com/github/yamdb/actions/workflows/yamdb_workflow.yml/badge.svg)

# Краткое описание проекта
YaMDb - программный интерфейс для социальной сети.
Он позволяет неравнодушным творческим людям обсудить заинтересовавшие их произведения: оставить отзывы к книгам, фильмам и т.д. и прокоментировать уже существующие отзывы 

## :dash: Установка и запуск проекта

### :dancers: Клонирование репозитория
git clone [SSH](git@github.com:Angelina91/infra_sp2.git)

### :whale: Запуск контейнеров
Из директории infra/
выполнить команду
docker-compose up -d --build

### :feet: Выполнить миграции
docker-compose exec web python manage.py migrate

### :bowtie: Создать суперпользователя
docker-compose exec web python manage.py createsuperuser

### :crystal_ball: Собрать статику
docker-compose exec web python manage.py collectstatic --no-input

### :love_letter: Заполнить базу данных
docker-compose exec web python manage.py loaddata ../infra/fixtures.json

## :dizzy: Стек
Rest Api, Docker, PostgreSQL

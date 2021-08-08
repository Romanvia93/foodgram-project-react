![example workflow](https://github.com/Romanvia93/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Description

Product Assistant app is a site where users can post recipes, add other people's recipes to favorites, and subscribe to other authors' publications. The Shopping List service will allow users to create a list of products that need to be purchased to prepare the selected dishes.

#### Проект доступен по адрессу
 [Foodgram](http://84.252.141.200/recipes)


# Running the project on the server

##### 1. Docker 
- Install [docker](https://docs.docker.com/engine/install/)
- Install [docker-compose](https://docs.docker.com/compose/install/)

##### 2. App running on Windows
Clone the repository with the command:
```sh
git clone https://github.com/Romanvia93/foodgram-project-react
```
Change to directory:
```sh
cd foodgram-project-react/infra/
```
Run the command to start the container:

```sh
docker-compose up -d --build
```

Apply migrations:
```sh
winpty docker-compose exec web python manage.py makemigration users
winpty docker-compose exec web python manage.py makemigration product
winpty docker-compose exec web python manage.py migrate
```

Collect statics:
```sh
winpty docker-compose exec web python manage.py collectstatic --no-input
```

Create superuser:
```sh
winpty docker-compose exec web python manage.py createsuperuser
```

# Software
- python 3.8
- django
- posgresql
- docker
- django-rest-framework

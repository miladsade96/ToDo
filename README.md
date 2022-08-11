# ToDo
Todo App Using Django


## How to run locally

1. Docker installation:  
[Install docker on your os](https://www.docker.com/)

2. Docker compose installation:  
[Install docker compose on your os](https://docs.docker.com/compose/install/)

3. Build the container and first run:
```shell
docker-compose up --build
```

4. Run the container:
```shell
docker-compose up
```

5. Make migrations:
```shell
docker-compose exec backend sh -c 'python manage.py makemigrations'
```

6. Migrate:
```shell
docker-compose exec backend sh -c 'python manage.py migrate'
```

7. Create a superuser:
```shell
docker-compose exec backend sh -c 'python manage.py createsuperuser'
```

8. Open the browser and go to https://127.0.0.1:8000/

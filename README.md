
## Description

Test task for the OneCorporated company. 

The project includes a system for receiving orders for the development of sites

You can:
 - authorize 
 - get/update profile
 - create/get news
 - create/list orders, attach some files

## Running the app

1. Create ```.env``` file and configure environmental variables

``` 
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=

# CELERY
CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
```

2. Run Programm
```bash
$ docker-compose up
```

### Functionality
You can check all endpoints in swagger
```
localhost:8000/swagger
```

# Simple Django CRUD Project

## Virtual Environment Setup
```cmd
conda create --no-default-packages -n <env_name>
conda activate <env_name>
conda install python=3.9
```

## Create Django Project
```cmd
django-admin startproject simple_django
```

## Simplify setup (windows)
```cmd
move simple_django\manage.py .\
move simple_django\simple_django\* simple_django
rmdir /s /q simple_django\simple_django\
```

## Create Django App
```cmd
python manage.py startapp simple_app
```

## Run Django Server
```cmd
python manage.py runserver
```

# CREATES THE DATABASE
## Create Migration for new model
```cmd
python manage.py makemigrations
```

## Apply migration to create the "Person" table in the database
```cmd
python manage.py migrate
```

## Create form for adding and editing a person
```cmd
python manage.py migrate
```

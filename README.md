
# DJANGO RECOMMENDER SYSTEMS PROJECT

THIS PROJECT IS SUPPOSED TO BE A SIMPLE DJANGO PROJECT BUT IT WOULD BE A GREAT OPPORTUNITY TO APPLY RECOMMENDER SYSTEMS TO DJANGO WITH CRUD THAT IS ALSO CONNECTED TO AWS.

<br>

## TABLE OF CONTENTS
1. [Django Setup](#django_setup)
	1. [Virtual Environment Setup](#conda)
	2. [Simplify setup (windows)](#win_setup)
	3. [Create Django App](#django_app)
	4. [Run Django Server](#django_server)
2. [AWS Database Setup](#aws_db)

<br>

## DJANGO SETUP <a name="django_setup"></a>
### Virtual Environment Setup <a name="conda"></a>
```cmd
conda create --no-default-packages -n <env_name>
conda activate <env_name>
conda install python=3.9
```

### Create Django Project <a name="django_proj"></a>
```cmd
django-admin startproject simple_django
```

### Simplify setup (windows) <a name="win_setup"></a>
```cmd
move simple_django\manage.py .\
move simple_django\simple_django\* simple_django
rmdir /s /q simple_django\simple_django\
```

### Create Django App <a name="django_app"></a>
```cmd
python manage.py startapp simple_app
```

### Run Django Server <a name="django_server"></a>
```cmd
python manage.py runserver
```

<br>

## AWS Database Setup <a name="aws_db"></a>

### 1. Create AWS RDS PostgreSQL Database
- Create necessary tables

```postgresql
CREATE TABLE ratings (
            user_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            rating NUMERIC(2,1) NOT NULL,
            timestamp BIGINT NOT NULL
        );

CREATE TABLE user_rating (
   	rating_id SERIAL,
        	user_id INTEGER REFERENCES user_info (user_id),
        	movie_id INTEGER,
        	rating NUMERIC(2,1) NOT NULL,
        	PRIMARY KEY (user_id, movie_id)
    	);

CREATE TABLE user_info (
            user_id INTEGER PRIMARY KEY
        );
```

<br>

- Load csv to ratings table using psql
```cmd
\copy ratings(user_id, movie_id, rating, timestamp) FROM <path_to_csv> WITH (FORMAT CSV, HEADER);
```
**NOTE**: This is done so we can load easily the data to our tables. We can drop this later on to save space on AWS RDS.

<br>

- Load data to our two tables named user_rating and user_info from ratings table
```sql
INSERT INTO user_info (user_id)
SELECT DISTINCT user_id
FROM ratings;

INSERT INTO user_rating (user_id,movie_id,rating)
SELECT user_id,movie_id,rating
FROM ratings;
```

<br>

### 2. Create AWS RDS PostgreSQL Database

- Change settings.py in our django project

**FROM**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
**TO**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': <DATABASE_NAME>,
        'USER': <USER>,
        'PASSWORD': <PASSWORD>,
        'HOST': <HOST>,
        'PORT': <PORT>,
    }
}
```
**NOTE**: Necessary information can be obtained after creation of database in AWS RDS

<br>

- generate model.py
```cmd
python manage.py inspectdb > (path to models directory)\models.py
```
**NOTE**: Make some changes in models.py

<br>

- migrate
```cmd
python manage.py migrate
```

<br>







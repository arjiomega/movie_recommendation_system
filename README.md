

# Simple Django CRUD Project

# DJANGO RECOMMENDER SYSTEMS PROJECT

![project image](https://i.imgur.com/YSp0ZFm.png)

This project's purpose is to showcase recommendation system using machine learning by making an interactive website.
- **Database used**: AWS RDS Postgresql
- **Recommender system**: Content-based filter (collab filter will not work well because the data used only have user ratings up to year 2020 and this project shows updated movies)
- **Currently deployed on**: aws ec2

<br>
Access to the url is available upon request to prevent my recommender system api currently deployed on aws lambda to get abused since I am trying to prevent getting past free tier limitations.

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
CREATE TABLE temp_storage (
            user_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            rating NUMERIC(2,1) NOT NULL,
            timestamp BIGINT NOT NULL
        );

CREATE TABLE temp_storage2 (
            movie_id INTEGER PRIMARY KEY,
            imdb_id INTEGER,
            tmdb_id INTEGER
        );

CREATE TABLE movie_info (
		tmdb_id INTEGER PRIMARY KEY,
		title varchar(255)
);
```

<br>

- Load CSVs to ratings and movie_info table using psql
```cmd
\copy temp_storage(user_id, movie_id, rating, timestamp) FROM <path_to_csv> WITH (FORMAT CSV, HEADER);
\copy temp_storage2(movie_id, imdb_id, tmdb_id) FROM <path_to_csv> WITH (FORMAT CSV, HEADER);
\copy movie_info(tmdb_id, title) FROM /home/rjomega/github_new/E2E_PROJECTS/recommender_system/ML/data/movies_metadata_mini.csv WITH (FORMAT CSV, HEADER);
```
**NOTE**: This is done so we can load easily the data to our tables. We can drop this later on to save space on AWS RDS.

<br>
- Check if there are any null

```postgresql
-- COMBINE TWO TABLES TO GET tmdb_id for movie_id (CHECK IF THERE ARE ANY NULL)
SELECT temp1.user_id, temp1.movie_id, temp2.tmdb_id, temp1.rating
FROM temp_storage temp1
LEFT JOIN temp_storage2 temp2
ON temp1.movie_id = temp2.movie_id
WHERE temp2.tmdb_id IS NULL;

-- COUNT NULL tmdb_id (NULL COUNT = 13503)
SELECT COUNT(*) AS null_tmdb_count
FROM temp_storage temp1
LEFT JOIN temp_storage2 temp2
ON temp1.movie_id = temp2.movie_id
WHERE temp2.tmdb_id IS NULL;
```
<br>

- Load data to our two tables named user_rating and user_info from ratings table

```postgresql
-- CREATE USER_INFO TABLE
CREATE TABLE user_info (
            user_id INTEGER PRIMARY KEY,
			user_password varchar(20)
        );

-- INSERT TO USER_INFO TABLE user_id with tmdb
INSERT INTO user_info (user_id)
SELECT DISTINCT temp1.user_id
FROM temp_storage temp1
LEFT JOIN temp_storage2 temp2
ON temp1.movie_id = temp2.movie_id
WHERE temp2.tmdb_id IS NOT NULL;

-- CREATE USER_RATING TABLE
CREATE TABLE user_rating (
   	rating_id SERIAL,
        	user_id INTEGER REFERENCES user_info (user_id),
        	tmdb_id INTEGER,
        	rating NUMERIC(2,1),
        	PRIMARY KEY (user_id, tmdb_id)
    	);

-- ADD DATA WITHOUT tmdb_id == NULL
INSERT INTO user_rating (user_id,tmdb_id,rating)
SELECT DISTINCT ON (temp1.user_id, temp2.tmdb_id) temp1.user_id, temp2.tmdb_id, temp1.rating
FROM temp_storage temp1
LEFT JOIN temp_storage2 temp2
ON temp1.movie_id = temp2.movie_id
WHERE temp2.tmdb_id IS NOT NULL;
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
python manage.py inspectdb > <path to models directory>\models.py
```
**NOTE**: Make some changes in models.py

<br>

- migrate
```cmd
python manage.py migrate
```


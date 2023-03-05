from django.core.management.base import BaseCommand
import pandas as pd
#from simple_app.models import User,Movies_UserRating
from sqlalchemy import create_engine
import psycopg2

class Command(BaseCommand):

    def handle(self,*args,**options):
        # user_data_df = pd.read_csv('./data/ratings_small.csv',usecols=[f.name for f in Movies_UserRating._meta.fields])
        # engine = create_engine('sqlite:///db.sqlite3')

        # unique_users_df = pd.DataFrame({'userId':user_data_df['userId'].unique()})
        # unique_users_df.to_sql(User._meta.db_table,if_exists='append',con=engine,index=False)


        # user_data_df.to_sql(Movies_UserRating._meta.db_table,if_exists='append',con=engine,index=False) # or append

        conn = psycopg2.connect(
            host="database-1.ckucjpr0j4qy.ap-northeast-1.rds.amazonaws.com",
            port="5432",
            database="movie_recommender",
            user="rjomega",
            password="joseph123"
        )

        conn.autocommit = True
        cursor = conn.cursor()

        sql = '''
        CREATE TABLE user_info (
            user_id INTEGER PRIMARY KEY
        );
        '''

        #cursor.execute(sql)

        # add automatic id for django
        sql2 = '''
        CREATE TABLE UserRating (
            userId INTEGER REFERENCES User_info (userId),
            movieId INTEGER,
            rating NUMERIC(2,1),
            PRIMARY KEY (userId, movieId)
        );
        '''
        #cursor.execute(sql2)

        sql_temp = '''
        CREATE TABLE ratings (
            userId INTEGER,
            movieId INTEGER,
            rating NUMERIC(2,1),
            timestamp BIGINT
        );
        '''
        #cursor.execute(sql_temp)
        #conn.commit()
        # import os
        # print(os.getcwd())

        print("created ratings table")

        sql_temp2 = '''
        COPY ratings(userId,moveId,rating,timestamp)
        FROM 'C:\\Users\\rjome\\simple_django_project\\data\\ratings.csv'
        with (format csv,header);
        '''
        #cursor.execute(sql_temp2)

        with open('C:\\Users\\rjome\\simple_django_project\\data\\ratings.csv', 'r') as f:
            copy_sql = """
            COPY ratings(userid,movieid,rating,timestamp)
            FROM STDIN
            WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',')
            """
            cursor.copy_expert(copy_sql,f)
            conn.commit()


        print("loaded csv to ratings table")

        sql3 = '''
        INSERT INTO user_info (userId)
        SELECT DISTINCT userId
        FROM ratings
        '''
        cursor.execute(sql3)
        conn.commit()
        print("loaded data to user_info table")

        sql4 = '''
        INSERT INTO user_rating (userId,movieId,rating)
        SELECT userId,movieId,rating
        FROM ratings
        '''
        cursor.execute(sql4)
        conn.commit()
        print("loaded data to user_rating table")

        sql5 = '''select * from UserRating;'''
        #cursor.execute(sql5)

        # for i in cursor.fetchall():
        #     print(i)


        cursor.close()
        conn.close()
#from simple_app.models import Movies_UserRating

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
#from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
#from nltk.stem.snowball import SnowballStemmer
#from nltk.stem.wordnet import WordNetLemmatizer
#from nltk.corpus import wordnet
#from surprise import Reader, Dataset, SVD, evaluate

import warnings; warnings.simplefilter('ignore')
import sys
sys.path('./simple_app')

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_app.settings')
django.setup()

## Data Cleaning

user_data_df = pd.read_csv('./data/ratings.csv')




# # # Convert the DataFrame to a list of dictionaries
data = user_data_df.to_dict('records')

# Iterate over the list of dictionaries and create a new instance of the Person model for each dictionary
for item in data:
    user = Movies_UserRating(
        userId = item['userId'],
        movieId = item['movieId'],
        rating = item['rating'],
    )

    # Save the new instance to the database
    user.save()
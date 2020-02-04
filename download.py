import os
from tqdm import tqdm
from movies_analyzer.RecommendationDataset import RecommendationDataSet
from movies_analyzer.Movies import Movies
import json

# download all images from imdb  ased on movielens, this is very long query
# for 9000 could take about 6 hours, for all imdb (500,000) could take about 2 weeks.
recommendation_dataset = RecommendationDataSet(movies = Movies())

from imdb import IMDb
import urllib.request 
import pickle

ia = IMDb()

IMAGE_FOLDER = 'data/images'
DATA_FOLDER = 'data/movies'
# ecommendation_dataset.
try:
    os.mkdir(IMAGE_FOLDER)
except:
    print('folder exist')

try:
    os.mkdir(DATA_FOLDER)
except:
    print('folder exist')

# all imdb movies
for i in tqdm(recommendation_dataset.movies.data.index):
    i = i.replace('tt','')
    movie = ia.get_movie(i)
    urllib.request.urlretrieve(movie['cover url'], IMAGE_FOLDER + "/"+ str(i) + '.jpg')
    with open(DATA_FOLDER+"/"+i+".pkl","wb") as f:
        pickle.dump(movie,f)


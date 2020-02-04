from tqdm import tqdm
from movies_analyzer.RecommendationDataset import RecommendationDataSet
from movies_analyzer.Movies import Movies
from movies_analyzer.Imdb import get_imdb_movie


# download all images from imdb  ased on movielens, this is very long query
# for 9000 could take about 6 hours, for all imdb (500,000) could take about 2 weeks.
recommendation_dataset = RecommendationDataSet(movies = Movies())

# all imdb movies
for tmbdid in tqdm(recommendation_dataset.movies.data.index):
    tmbdid = tmbdid.replace('tt','')
    # get_imdb_movie(i)

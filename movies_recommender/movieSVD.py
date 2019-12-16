import csv
from collections import defaultdict

import learn as learn
from surprise import SVD
from surprise.model_selection import GridSearchCV
import pandas as pd
from surprise.model_selection import train_test_split
from surprise import Dataset
from surprise import Reader
from surprise import accuracy



if __name__ == '__main__':
    ratingsPath = '/home/krzysztof/Pobrane/ml-latest-small/ratings.csv'
    reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)
    ratingsDataset = Dataset.load_from_file(ratingsPath, reader=reader)

    param_grid = {'n_epochs': [20, 30], 'lr_all': [0.005, 0.010],
              'n_factors': [50, 100]}
    gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)

    gs.fit(ratingsDataset)

    # best RMSE score
    print("Best RMSE score attained: ", gs.best_score['rmse'])

    # combination of parameters that gave the best RMSE score
    print(gs.best_params['rmse'])

    params = gs.best_params['rmse']
    SVDtuned = SVD(n_epochs=params['n_epochs'], lr_all=params['lr_all'], n_factors=params['n_factors'])
    trainSet, testSet = train_test_split(ratingsDataset, test_size=.2, random_state=1)
    SVDtuned.fit(trainSet)
    predictions = SVDtuned.test(testSet)
    rmse = accuracy.rmse(predictions, verbose=False)
    mae = accuracy.mae(predictions, verbose=False)
    print(f'RMSE: {rmse}' )
    print(f'MAE: {mae}' )

    movies = pd.read_csv('/home/krzysztof/Pobrane/ml-latest-small/movies.csv')
    recomendation = pd.DataFrame(columns=['Movie','Rating'])
    i = 0
    for userID, movieID, actualRating, estimatedRating, _ in predictions:
        recomendation.loc[i] = [movies[movies['movieId']==int(movieID)]['title'].to_list()[0], estimatedRating ]
        i = i + 1

    recomendation['Rating'] = pd.to_numeric(recomendation['Rating'])
    recomendation.sort_values(by=['Rating'])
    print(recomendation.head(10))
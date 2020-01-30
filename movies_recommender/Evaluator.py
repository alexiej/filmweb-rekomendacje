from surprise import accuracy
from collections import defaultdict
from movies_recommender.utils import get_top_n


def HitRate(topNPredicted, leftOutPredictions):
    hits = 0
    total = 0

    # For each left-out rating
    for leftOut in leftOutPredictions:
        userID = leftOut[0]
        leftOutMovieID = leftOut[1]
        # Is it in the predicted top 10 for this user?
        hit = False
        for movieID, predictedRating in topNPredicted[int(userID)]:
            if (int(leftOutMovieID) == int(movieID)):
                hit = True
                break
        if (hit):
            hits += 1

        total += 1

    # Compute overall precision
    return hits / total


def CumulativeHitRate(topNPredicted, leftOutPredictions, ratingCutoff=0):
    hits = 0
    total = 0

    # For each left-out rating
    for userID, leftOutMovieID, actualRating, estimatedRating, _ in leftOutPredictions:
        # Only look at ability to recommend things the users actually liked...
        if (actualRating >= ratingCutoff):
            # Is it in the predicted top 10 for this user?
            hit = False
            for movieID, predictedRating in topNPredicted[int(userID)]:
                if (int(leftOutMovieID) == movieID):
                    hit = True
                    break
            if (hit):
                hits += 1

            total += 1

    # Compute overall precision
    return hits / total


def RatingHitRate(topNPredicted, leftOutPredictions):
    hits = defaultdict(float)
    total = defaultdict(float)

    # For each left-out rating
    for userID, leftOutMovieID, actualRating, estimatedRating, _ in leftOutPredictions:
        # Is it in the predicted top N for this user?
        hit = False
        for movieID, predictedRating in topNPredicted[int(userID)]:
            if (int(leftOutMovieID) == movieID):
                hit = True
                break
        if (hit):
            hits[actualRating] += 1

        total[actualRating] += 1

    # Compute overall precision
    ratings = {}
    for rating in sorted(hits.keys()):
        ratings[rating] = hits[rating] / total[rating]
    return ratings


def AverageReciprocalHitRank(topNPredicted, leftOutPredictions):
    summation = 0
    total = 0
    # For each left-out rating
    for userID, leftOutMovieID, actualRating, estimatedRating, _ in leftOutPredictions:
        # Is it in the predicted top N for this user?
        hitRank = 0
        rank = 0
        for movieID, predictedRating in topNPredicted[int(userID)]:
            rank = rank + 1
            if (int(leftOutMovieID) == movieID):
                hitRank = rank
                break
        if (hitRank > 0):
            summation += 1.0 / hitRank

        total += 1

    return summation / total


# What percentage of users have at least one "good" recommendation
def UserCoverage(topNPredicted, numUsers, ratingThreshold=0):
    hits = 0
    for userID in topNPredicted.keys():
        hit = False
        for movieID, predictedRating in topNPredicted[userID]:
            if (predictedRating >= ratingThreshold):
                hit = True
                break
        if (hit):
            hits += 1

    return hits / numUsers


import itertools


def Diversity(topNPredicted, simsAlgo, fun=int):
    n = 0
    total = 0
    simsMatrix = simsAlgo.compute_similarities()
    for userID in topNPredicted.keys():
        pairs = itertools.combinations(topNPredicted[userID], 2)
        for pair in pairs:
            movie1 = pair[0][0]
            movie2 = pair[1][0]
            innerID1 = simsAlgo.trainset.to_inner_iid(fun(movie1))
            innerID2 = simsAlgo.trainset.to_inner_iid(fun(movie2))
            similarity = simsMatrix[innerID1][innerID2]
            total += similarity
            n += 1

    S = total / n
    return 1 - S


def Novelty(topNPredicted, rankings):
    n = 0
    total = 0
    for userID in topNPredicted.keys():
        for rating in topNPredicted[userID]:
            movieID = rating[0]
            rank = rankings[int(movieID)]
            total += rank
            n += 1
    return total / n


def get_evaluation(recommender: 'Recommender', verbose=True, anti_test=True):
    # algorithm = recommender.algorithm
    recommendation_dataset = recommender.recommendation_dataset

    metrics = {}
    if verbose: print('Precalculations')
    recommender.fit(recommendation_dataset.train_set)
    predictions = recommender.test(recommendation_dataset.test_set)

    if verbose: print('calculating MAE, RMSE')
    metrics['MAE'] = accuracy.mae(predictions, verbose=False)
    metrics['RMSE'] = accuracy.rmse(predictions, verbose=False)

    if anti_test:
        # LEAVE ONE OUT FIT/TEST
        if verbose: print('LEAVE ONE OUT FIT/TEST')
        recommender.fit(recommendation_dataset.leave_one_out_train_set)
        leave_one_out_test_prediction = recommender.test(recommendation_dataset.leave_one_out_test_set)

        #  LEAVE ONE OUT ANTI TEST PREDICTION/TOP-N
        if verbose: print('LEAVE ONE OUT ANTI TEST PREDICTION/TOP-N, very long calculation')
        leave_one_out_anti_test_prediction = recommender.test(recommendation_dataset.leave_one_out_anti_test_set)
        leave_one_out_anti_test_topn = get_top_n(leave_one_out_anti_test_prediction, 10, 4.0)

        # See how often we recommended a movie the user actually rated
        if verbose: print('HR')
        metrics["HR"] = HitRate(leave_one_out_anti_test_topn, leave_one_out_test_prediction)

        # See how often we recommended a movie the user actually liked
        if verbose: print('cHR')
        metrics["cHR"] = CumulativeHitRate(leave_one_out_anti_test_topn, leave_one_out_test_prediction)

        # Compute ARHR
        if verbose: print('ARHR')
        metrics["ARHR"] = AverageReciprocalHitRank(leave_one_out_anti_test_topn, leave_one_out_test_prediction)

        # Rating HitRate
        if verbose: print('rHR')
        metrics["rHR"] = RatingHitRate(leave_one_out_anti_test_topn, leave_one_out_test_prediction)

    # BASED ON FULL DATASET
    if verbose: print('BASED ON FULL DATASET')
    recommender.fit(recommendation_dataset.full_dataset)
    anti_test_prediction = recommender.test(recommendation_dataset.anti_test_set)
    anti_test_topn = get_top_n(anti_test_prediction, 10, 4.0)

    # Coverage
    if verbose: print('Coverage')
    metrics["Coverage"] = UserCoverage(anti_test_topn,
                                       recommendation_dataset.full_dataset.n_users,
                                       ratingThreshold=4.0)

    # Measure diversity of recommendations:
    if verbose: print('Diversity')
    metrics["Diversity"] = Diversity(anti_test_topn,
                                     recommendation_dataset.similarity_algorithm, str)

    # Measure novelty (average popularity rank of recommendations):
    if verbose: print('Novelty')
    metrics["Novelty"] = Novelty(anti_test_topn, recommendation_dataset.rankings)

    if verbose:
        print('Mean Absolute Error:', metrics['MAE'])
        print('Root Mean Square Error:', metrics['RMSE'])

        print('Hit Rate (HR):', metrics['HR'])
        print('Cumulative Hit Rate (cHR):', metrics['cHR'])
        print('Average Reciprocal HitRate  (ARHR):', metrics['ARHR'])

        print('Rating  HitRate  (rHR):', metrics['rHR'])

        print('Coverage:', metrics['Coverage'])
        print('Diversity:', metrics['Diversity'])
        print('Novelty:', metrics['Novelty'])

    return metrics

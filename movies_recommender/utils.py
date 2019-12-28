from collections import defaultdict


# https://surprise.readthedocs.io/en/stable/FAQ.html#how-to-get-the-top-n-recommendations-for-each-user
def get_top_n(predictions, n=10, minimum_rating=4.0):
    top_n = defaultdict(list)

    for userID, movieID, actualRating, estimatedRating, _ in predictions:
        if estimatedRating >= minimum_rating:
            top_n[int(userID)].append((int(movieID), estimatedRating))

    for userID, ratings in top_n.items():
        ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[int(userID)] = ratings[:n]

    return top_n


def get_popularity_ranking(data):
    ratings = defaultdict(int)
    rankings = defaultdict(int)

    for userId, movieId, _ in data.all_ratings():
        ratings[movieId] += 1
    rank = 1
    for movieId, _ in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
        rankings[int(data.to_raw_iid(movieId))] = rank
        rank += 1
    return ratings, rankings

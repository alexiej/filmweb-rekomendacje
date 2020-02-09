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



import sys
from types import ModuleType, FunctionType
from gc import get_referents

# Custom objects know their class.
# Function objects seem to know way too much, including modules.
# Exclude modules as well.
BLACKLIST = type, ModuleType, FunctionType


def getsize(obj):
    """sum size of object & members."""
    if isinstance(obj, BLACKLIST):
        raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return str(float(size)/(1024*1024)) + " MB"
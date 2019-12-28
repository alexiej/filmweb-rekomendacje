import os

from movies_analyzer.Imdb import Imdb
from filmweb_integrator.fwimdbmerge.utils import get_logger

logger = get_logger()

# logger.warning("Start import example_mateusz_01_json.csv")
# os.system("wget -O data/example_mateusz_01_json.csv https://raw.githubusercontent.com/mateuszrusin/ml-filmweb-score/master/oceny.csv")
# logger.warning("Start import genre.txt")
# os.system("wget -O data/genre.txt https://raw.githubusercontent.com/dataworkshop/dw-poznan-project/master/spotkania/2019-11-12/wykresy/genre.txt")

logger.warning("Download MovieLens Database")
os.system("wget -O data/ml-latest-small.zip http://files.grouplens.org/datasets/movielens/ml-latest-small.zip")
os.system("unzip data/ml-latest-small.zip -d data")
logger.warning("Done")


logger.warning("Start imdb prepare")
Imdb.prepare()
logger.warning("Done")

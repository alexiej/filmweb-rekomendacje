import os

from filmweb_integrator.fwimdbmerge.imdb import Imdb
from filmweb_integrator.fwimdbmerge.utils import get_logger

logger = get_logger()

# logger.warning("Start import example_mariusz_02_filmeb.csv")
# os.system("wget -O data/example_mariusz_02_filmeb.csv https://raw.githubusercontent.com/mateuszrusin/ml-filmweb-score/master/oceny.csv")
# logger.warning("Start import genre.txt")
# os.system("wget -O data/genre.txt https://raw.githubusercontent.com/dataworkshop/dw-poznan-project/master/spotkania/2019-11-12/wykresy/genre.txt")

logger.warning("Start imdb prepare")
Imdb.prepare()
logger.warning("Done")

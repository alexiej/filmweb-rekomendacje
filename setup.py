import os

from filmweb_integrator.fwimdbmerge.imdb import Imdb


os.system("wget -O data/oceny.csv https://raw.githubusercontent.com/mateuszrusin/ml-filmweb-score/master/oceny.csv")
os.system("wget -O data/genre.txt https://raw.githubusercontent.com/dataworkshop/dw-poznan-project/master/spotkania/2019-11-12/wykresy/genre.txt")

Imdb.prepare()

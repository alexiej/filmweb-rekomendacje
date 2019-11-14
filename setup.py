import os

os.system("wget -O data/oceny.csv https://raw.githubusercontent.com/mateuszrusin/ml-filmweb-score/master/oceny.csv")
os.system("wget -O data/title.basics.tsv.gz https://datasets.imdbws.com/title.basics.tsv.gz")
os.system("wget -O data/title.ratings.tsv.gz https://datasets.imdbws.com/title.ratings.tsv.gz")
os.system("gzip -d -f data/title.basics.tsv.gz")
os.system("gzip -d -f data/title.ratings.tsv.gz")
os.system(
    "wget -O data/genre.txt https://raw.githubusercontent.com/dataworkshop/dw-poznan-project/master/spotkania/2019-11-12/wykresy/genre.txt")

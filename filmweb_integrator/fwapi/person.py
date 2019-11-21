# coding=utf-8
import datetime

from collections import OrderedDict
from functools import total_ordering

from .base import FilmwebObject
from .utils import make_request


@total_ordering
class Person(FilmwebObject):
    def __init__(self, name, url):
        super(Person, self).__init__(url, name)
        
        self.name = name
        self.url = url
        
        self.full_name = None
        self.birth_date = None
        self.filmography = None
    
    @staticmethod
    def parse_full_name(soup):
        return soup.select("div.personMainHeader")[0].h2.text

    @staticmethod
    def parse_birth_date(soup):
        bd = soup.select('span[itemprop="birthDate"]')[0]["content"]
        return datetime.datetime.strptime(bd, "%Y-%m-%d").date()

    @staticmethod
    def parse_filmography(soup):
        """
        Returns a dictionary with entries in the following form:
         (Film's title (role, year of production))
        """
        filmography = OrderedDict()
        film_data = soup.select('tr[data-type="F"]')
        for f in film_data:
            year = int(f.span.text)
            title = f.a.text
            character = f.p.text if f.p is not None else ""
            filmography.update({title: (character, year)})
        return filmography
    
    def populate(self):
        """
        Populates more detailed fields that remain empty (None) after the object's instantiation
        """
        soup = make_request(self.url)

        self.full_name = self.parse_full_name(soup)
        self.birth_date = self.parse_birth_date(soup)
        self.filmography = self.parse_filmography(soup)
        
    def __repr__(self):
        return "<{}>".format(self.name)
    
    def __eq__(self, other):
        return self.name.lower() == other.name.lower()
    
    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

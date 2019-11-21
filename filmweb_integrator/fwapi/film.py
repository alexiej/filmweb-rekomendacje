# coding=utf-8
import datetime
import re

from functools import total_ordering

from .base import FilmwebObject
from .utils import make_request


@total_ordering
class Film(FilmwebObject):
    
    def __init__(self, url, title, year, id_):
        super(Film, self).__init__(url, title, year, id_)
      
        self.title = title
        self.year = year
        self.id_ = id_

        self.actors = None
        self.country = None
        self.description = None
        self.director = None
        self.duration = None
        self.genre = None
        self.original_title = None
        self.screenwriter = None
        self.boxoffice = None
        self.budget = None
        self.topics_count = None

    @classmethod
    def get_by_id(cls, id_):
        """
        Gets the film by using its id. Returns a Film object.
        """
        url = "http://www.filmweb.pl/Film?id={}".format(id_)
        soup = make_request(url)
        if soup.title.text.startswith("Nie znaleziono"):
            return None
        film_data = soup.h1.a
        title = film_data["title"]
        link = "http://www.filmweb.pl" + film_data["href"]
        year = film_data.next_sibling.next_sibling.text.strip("(").strip(") ")
        film = cls(url=link, title=title, year=int(year), id_=id_)
        return film

    @staticmethod
    def parse_actors(soup):
        actors = soup.select("table.filmCast")[0].select("a.pImg46")
        characters = soup.select('span[itemprop="characterName"]')
        actor_names = (a["title"] for a in actors)
        char_names = (ch.text.strip() for ch in characters)
        results = dict(zip(actor_names, char_names))
        return results

    @staticmethod
    def parse_country(soup):
        """
        Gets a list of countries participating in making the film
        """
        found = soup.select("ul.genresList")[0].parent.parent.next_sibling.find_all("a")
        countries = [c.text for c in found]
        return countries

    @staticmethod
    def parse_description(soup):
        descr = soup.select(".filmPlot")
        if len(descr) > 0:
            descr = descr[0].p.text
        else:
            descr = ""
        return descr

    @staticmethod
    def parse_director(soup):
        """
        Gets a list of directors
        """
        found = soup.select('a[itemprop="name"]')
        directors = [d.text for d in found]
        return directors

    @staticmethod
    def parse_duration(soup):
        duration = soup.time.text
        pattern = re.compile(r'((\d{1,2}) godz.)? (\d{1,2}) min.')
        match = pattern.match(duration)
        if match:
            matches = match.groups()
            hours, minutes = matches[1], matches[2]
            if hours is None:
                hours = 0
            return datetime.time(int(hours), int(minutes))
        return None

    @staticmethod
    def parse_genre(soup):
        """
        Gets a list of genres
        """
        found = soup.select("ul.genresList")[0].find_all("a")
        genres = [g.text for g in found]
        return genres

    @staticmethod
    def parse_original_title(soup):
        """
        Gets the original title
        """
        try:
            return soup.select("h2.cap")[0].text
        except IndexError:
            return None

    @staticmethod
    def parse_screenwriter(soup):
        """
        Gets a list of screenwriters
        """
        found = soup.select('a[itemprop="name"]')[0].parent.parent.parent.parent.next_sibling.find_all("a")
        screenwriters = [sw.text for sw in found]
        return screenwriters

    @staticmethod
    def parse_boxoffice(soup):
        """
        Gets a boxoffice sum in dollars
        """
        element = soup.find(text='boxoffice:')
        if element:
            boxoffice = element.parent.next_sibling
            for val in boxoffice.children:
                if val:
                    return int(''.join([n for n in val.string if n.isdigit()]))
        return None

    @staticmethod
    def parse_budget(soup):
        """
        Gets a budget sum in dollars
        """
        try:
            found = soup.find(text='budżet:').parent.next_sibling.text
            return int(''.join([n for n in found if n.isdigit()]))
        except Exception:
            return None

    @staticmethod
    def parse_topics(soup):
        """
        Gets a forum topics count
        """
        try:
            found = soup.select('.forum-name span')[0].text
            return int(''.join([n for n in found if n.isdigit()]))
        except Exception:
            return None

    def populate(self):
        """
        Populates more detailed fields that remain empty (None) after the object's instantiation
        """
        soup = make_request(self.url)

        self.actors = self.parse_actors(soup)
        self.country = self.parse_country(soup)
        self.description = self.parse_description(soup)
        self.director = self.parse_director(soup)
        self.duration = self.parse_duration(soup)
        self.genre = self.parse_genre(soup)
        self.original_title = self.parse_original_title(soup)
        self.screenwriter = self.parse_screenwriter(soup)
        self.boxoffice = self.parse_boxoffice(soup)
        self.budget = self.parse_budget(soup)
        self.topics_count = self.parse_topics(soup)

    def __repr__(self):
        return "<{}: {}>".format(self.title, self.year)
        
    def __eq__(self, other):
        return self.id_ == other.id_
    
    def __lt__(self, other):
        return self.title.lower() < other.title.lower()

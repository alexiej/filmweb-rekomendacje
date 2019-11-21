# coding=utf-8

from  filmweb_integrator.fwapi.utils import make_request

class FilmwebObject:
    
    def __init__(self, url, *args):
        self.url = url
    
    @classmethod
    def search(cls, phrase, max_page=1):
        """
        Searches for object based on the title/name. Returns a list of
        Film/Person objects with matching 'title'/'name' attributes.

        max_page = indicates from how many pages of search results
                   data will be extracted
        """
        page = 1
        
        #final_results = []
        while page <= max_page:
            url = "http://www.filmweb.pl/search/{}?q={}&page={}".format(cls.__name__.lower(), phrase, page)

            soup = make_request(url)

            if cls.__name__ == "Film":
                results = soup.select("a.filmPreview__link")
            elif cls.__name__ == "Person":
                results = soup.select(".hit__desc a")
            else:
                results = []

            for res in results:
                obj = None
                name = res.text.strip()
                link = "http://www.filmweb.pl" + res["href"]
                
                if cls.__name__ == "Film":
                    year = int(res.next_sibling.next_sibling.text)
                    id_ = int(res.parent.parent.parent.parent["data-id"])
                    obj = cls(title=name, url=link, year=int(year), id_=int(id_))
                    
                elif cls.__name__ == "Person":
                    obj = cls(name=name, url=link)
                    
                yield obj
            
            page += 1


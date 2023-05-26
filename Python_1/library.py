from datetime import datetime
import jsons

class Book():
    def __init__(self, title, author, page_number, purchase_price, purchase_year):
       self.title = title
       self.author = author
       self.page_number = page_number
       self.purchase_price = purchase_price
       self.purchase_year = purchase_year

    def current_value(self):
        y_year_now = datetime.today().year
        y_year_bought = self.purchase_year
        value = self.purchase_price
        if y_year_now - y_year_bought > 50:
            while y_year_now > y_year_bought:
                value = value - value * 1.08
                y_year_bought = y_year_bought + 1
        else:
            while y_year_now > y_year_bought:
                value = value - value * 0.1
                y_year_bought = y_year_bought + 1
        return round(value, 2)


class Movie():
    def __init__(self, title, director, length, purchase_price, purchase_year, quality):
        self.title = title
        self.director = director
        self.length = length
        self.purchase_price = purchase_price
        self.purchase_year = purchase_year
        self.quality = quality

    def current_value(self):
        y_year_now = datetime.today().year
        y_year_bought = self.purchase_year
        value = self.purchase_price
        while y_year_now > y_year_bought:
            value = value - value * 0.1
            y_year_bought = y_year_bought + 1
        return round(value * (self.quality/10), 2)


class CD():
    def __init__(self, title, artist, tracks, length, purchase_price):
        self.title = title
        self.artist = artist
        self.tracks = tracks
        self.length = length
        self.purchase_price = purchase_price

    def current_value(self, library):
        num_similar = len(library.find_cds(self.title, self.artist))
        return round(self.purchase_price / num_similar, 0)


class Library:
    def __init__(self):
        self.books = []
        self.movies = []
        self.cds = []

    def find_cds(self, title, artist):
        ret = []
        for cd in self.cds:
            if cd.title == title and cd.artist == artist:
                ret.append(cd)
        return ret

    def new_book(self, title, author, page_number, purchase_price, purchase_year):
        self.books.append(Book(title, author, page_number, purchase_price, purchase_year))

    def new_movie(self, title, director, length, purchase_price, purchase_year, quality):
        self.movies.append(Movie(title, director, length, purchase_price, purchase_year, quality))

    def new_cd(self, title, artist, tracks, length, purchase_price):
        self.cds.append(CD(title, artist, tracks, length, purchase_price))

    def get_cds(self):
        return self.cds

    def get_books(self):
        return self.books

    def get_movies(self):
        return self.movies

    def get_all(self):
        return self.books + self.movies + self.cds

    def store_inventory(self):
        entities = {
            "books" : self.books,
            "movies": self.movies,
            "cds"   : self.cds
            }

        with open('data.json', 'w') as f:
            f.write(jsons.dumps(entities))   

    def load_inventory(self):
        try:
             with open('data.json', 'r') as f:
                data = jsons.loads(f.read())
                for book in data['books']:
                    b = Book(book['title'], book['author'], book['page_number'], book['purchase_price'], book['purchase_year'])
                    self.books.append(b)
                for movie in data['movies']:
                    m = Movie(movie['title'], movie['director'], movie['length'], movie['purchase_price'], movie['purchase_year'], movie['quality'])
                    self.movies.append(m)
                for cd in data['cds']:
                    c = CD(cd['title'], cd['artist'], cd['tracks'], cd['length'], cd['purchase_price'])
                    self.cds.append(c)

        except Exception:
                pass

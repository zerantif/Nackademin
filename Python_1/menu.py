import sys
import library

class Menu:
    def __init__(self):
        self.library = library.Library()
        self.choices = {
            "1" : [ "Register a Book", self.add_book ],
            "2" : [ "Register a Movie", self.add_movie ],
            "3" : [ "Register a CD", self.add_cd ],
            "4" : [ "Present Books", self.present_books ],
            "5" : [ "Present Movies", self.present_movies ],
            "6" : [ "Present CDs", self.present_cds ],
            "7" : [ "Present All", self.present_all ],
            "8" : [ "Present All Sorted", self.present_all_sorted],
            "9" : [ "Save & Quit program", self.quit ]
            }

    def display_menu(self):
        print("Library Menu")
        for item in self.choices:
            print(f"    {item}. {self.choices[item][0]}")

    def input_int(self, prompt, max_value=None):
        ret = None
        while ret is None:
            try:
                ret = int(input(prompt))
                if max_value is not None:
                    if max_value < ret:
                        print(f"Maximum number is {max_value}. Try again.")
                        ret = None
            except ValueError:
                print("Error. Must supply integer value.")
        return ret

    def run(self):
        self.library.load_inventory()
        while True:
            print()
            self.display_menu()
            choice = input("Enter a menu option: ")
            action = self.choices.get(choice)
            if action:
                action[1]()
            else:
                print(f"{choice} is not a valid choice!")
                print()

    def add_book(self):
        title = input("Enter the title: ").capitalize()
        author = input("Enter the author's name: ").capitalize()
        page_number = self.input_int("Enter pagenumbers: ", 10000)
        purchase_price = self.input_int("Enter the purchase price (SEK): ")
        purchase_year = self.input_int("Enter the purchase year: ", 2100)
        self.library.new_book(title, author, page_number, purchase_price, purchase_year)
        print()
        print("Your book has been registred")

    def add_movie(self):
        title = input("Enter the title: ").capitalize()
        director = input("Enter the director's name: ").capitalize()
        length = self.input_int("Enter the length of the movie (minutes): ", 1000)
        purchase_price = self.input_int("Enter the purchase price (SEK): ")
        purchase_year = self.input_int("Enter the purchase year: ", 2100)
        quality = self.input_int("Quality (1-10): ", 10)
        self.library.new_movie(title, director, length, purchase_price, purchase_year, quality)
        print()
        print("Your movie has been registered.")

    def add_cd(self):
        title = input("Enter the title: ").capitalize()
        artist = input("Enter the artist's name: ").capitalize()
        tracks = self.input_int("Enter the number of tracks: ", 1000)
        length = self.input_int("Enter the CD's length (minutes): ", 1000)
        purchase_price = self.input_int("Enter the purchase price (SEK): ")
        self.library.new_cd(title, artist, tracks, length, purchase_price)
        print()
        print("Your cd has been registered.")

    def present_items(self, items):
        for item in items:
            if isinstance(item, library.Book):
                print(f"Book  {item.title:19} {item.author:20}  {item.page_number:5} pages              {item.purchase_price:3} kr         {item.purchase_year:4}          {item.current_value():7} kr")
            if isinstance(item, library.CD):
                print(f"CD    {item.title:19} {item.artist:20} {item.tracks:5} tracks   {item.length:5} min  {item.purchase_price:3} kr                        {item.current_value(self.library):7} kr")
            if isinstance(item, library.Movie):
                print(f"Movie {item.title:19} {item.director:20}                {item.length:5} min  {item.purchase_price:3} kr         {item.purchase_year:4}           {item.current_value():7} kr")

    def present_books(self, print_header=True):
        if print_header:
            print("Type  Titel               Author                  Pages                  Purchase price Purchased year  Current value")
            print("=====================================================================================================================")
        self.present_items(self.library.get_books())

    def present_movies(self, print_header=True):
        if print_header:
            print("Type  Titel               Director                              Runtime  Purchase price Purchased year  Current value")
            print("=====================================================================================================================")
        self.present_items(self.library.get_movies())
            
    def present_cds(self, print_header=True):
        if print_header:
            print("Type  Titel               Artist                  Tracks        Runtime  Purchase price                 Current value")
            print("=====================================================================================================================")
        self.present_items(self.library.get_cds())

    def present_all(self):
        print("Type  Titel               Auth./Director/Artist   Pages/Tracks  Runtime  Purchase price Purchased year  Current value")
        print("=====================================================================================================================")
        self.present_books(False)
        self.present_movies(False)
        self.present_cds(False)

    def present_all_sorted(self):
        print("Type  Titel               Auth./Director/Artist   Pages/Tracks  Runtime  Purchase price Purchased year  Current value")
        print("=====================================================================================================================")
        sorted_list = sorted(self.library.get_all(), key=lambda x: x.title)
        self.present_items(sorted_list)

    def quit(self):  
        print()
        self.library.store_inventory()
        print("Data saved!")
        print("Thank you for using the library.")
        print()
        sys.exit(0)

if __name__ == "__main__":
    Menu().run()

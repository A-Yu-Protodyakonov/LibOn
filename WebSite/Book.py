#from interface import Interface, implements
from LibraryElement import LibraryElement


class Book(LibraryElement):
    id, Author, publish_year,rentalTime, type = None, None, None, None, None

    def __init__(self, id_book, name, rubric, author, publish_year, rentalTime, type_t):
        super(Book, self).__init__(name, rubric)
        self.id = id_book
        self.Author = author.lower().title()
        self.publish_year = publish_year
        self.rentalTime = rentalTime
        if type_t == 'on':
            self.type = 2
        else:
            self.type = 1

    def get_type(self):
        if self.type == 2:
            return 'электронная'
        else:
            return 'печатная'

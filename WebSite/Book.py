#from interface import Interface, implements
from LibraryElement import LibraryElement


class Book(LibraryElement):
    id, Author, rentalTime, type = None, None, None, None

    def __init__(self, id_book, name, rubric, author, rentalTime, type_t):
        super(Book, self).__init__(name, rubric)
        self.id = id_book
        self.Author = author
        self.rentalTime = rentalTime
        self.type = type_t

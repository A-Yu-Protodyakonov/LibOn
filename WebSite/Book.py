from interface import Interface, implements
from LibraryElement import LibraryElement


class Book(LibraryElement):
    Author = None
    rentalTime = None
    type = None

    def __init__(self, name, rubric, author, rentalTime, type):
        super(Book, self).__init__(name, rubric)
        self.Author = author
        self.rentalTime = rentalTime
        self.type = type

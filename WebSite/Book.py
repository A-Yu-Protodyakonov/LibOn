from interface import Interface, implements
from LibraryElement import *


class Book(implements(LibraryElement)):
    Author = None
    rentalTime = None
    type = None
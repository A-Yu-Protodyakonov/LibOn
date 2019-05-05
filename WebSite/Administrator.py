from interface import Interface, implements
from SystemMember import SystemMember


class Administrator(SystemMember):
    email, password = None, None

    def add_book(self, new_book):
        self.add(new_book)

    def delete_book(self, book):
        self.delete(book)

    def change_book(self, book):
        self.change(book)


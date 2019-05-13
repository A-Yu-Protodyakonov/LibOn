from interface import Interface, implements
from SystemMember import SystemMember


class Administrator(SystemMember):
    email, password = None, None

    def __init__(self, name, lastName, email, password):
        super(Administrator, self).__init__(name, lastName)
        self.email = email
        self.password = password

    def add_book(self, new_book):
        self.add(new_book)

    def delete_book(self, book):
        self.delete(book)

    def change_book(self, book):
        self.change(book)

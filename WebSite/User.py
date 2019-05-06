from interface import Interface, implements
from SystemMember import SystemMember


class User(implements(SystemMember)):
    email, order_list, password = None, None, None

    def add_to_order(self, new_book):
        self.add(new_book)

    def delete_from_order(self, book):
        self.delete(book)

    def set_email(self, e_mail):
        self.email = e_mail
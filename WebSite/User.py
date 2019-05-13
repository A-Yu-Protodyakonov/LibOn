from interface import Interface, implements
from SystemMember import SystemMember


class User(SystemMember):
    email, order_list, password = None, None, None

    def __init__(self, name, lastname, email, orderList, password):
        super(User, self).__init__(name, lastname)
        self.email = email
        self.order_list = orderList
        self.password = password

    def add_to_order(self, new_book):
        self.add(new_book)

    def delete_from_order(self, book):
        self.delete(book)

    def set_email(self, e_mail):
        self.email = e_mail
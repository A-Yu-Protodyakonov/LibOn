#from interface import Interface, implements
from SystemMember import SystemMember
from Book import Book
import sqlite3
import os
import datetime


class User(SystemMember):
    id, email, order_list, password = None, None, None, None
    Database = os.path.join(os.path.dirname(__file__), 'PT.db')

    def __init__(self, id_member, name, lastname, email, orderList, password):
        super(User, self).__init__(name, lastname)
        self.id = id_member
        self.email = email
        self.order_list = orderList
        self.password = password

    def add_to_order(self, new_book: Book):
        now = datetime.datetime.now()
        connect = sqlite3.connect(self.Database)
        cursor = connect.cursor()
        cursor.execute("INSERT INTO _ORDER (START_DATE, BOOK_ID, USER_ID) VALUES ({}, {}, {}); ".format(
            now.strftime("%d-%m-%Y"), new_book.id, self.id))
        connect.commit()

    def delete_from_order(self, book: Book):
        connect = sqlite3.connect(self.Database)
        cursor = connect.cursor()
        order_id = cursor.execute("select ORDER_ID from _ORDER where BOOK_ID = {} and USER_ID = {}; ".format(
            book.id, self.id)).fetchone()
        cursor.execute("delete from _ORDER where ORDER_ID = {};".format(order_id))
        connect.commit()

    def set_email(self, e_mail):
        connect = sqlite3.connect(self.Database)
        cursor = connect.cursor()
        cursor.execute("update USER set E_MAIL = {}, where USER_ID = {};".format(e_mail, self.id))
        connect.commit()


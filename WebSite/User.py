#from interface import Interface, implements
from SystemMember import SystemMember
from Book import Book
import sqlite3
import os
from _datetime import date,datetime


class User(SystemMember):
    id, email,  password = None, None, None
    Database = os.path.join(os.path.dirname(__file__), 'PT.db')

    def __init__(self, id_member, name, lastname, email, password):
        super(User, self).__init__(name, lastname)
        self.id = id_member
        self.email = email
        self.password = password

    def add_to_order(self, book_id):
        now = date.today()
        connect = sqlite3.connect(self.Database)
        cursor = connect.cursor()
        cursor.execute("INSERT INTO _ORDER (START_DATE, BOOK_ID, USER_ID) VALUES (\"{}\", {}, {}); ".format(
            now, book_id, self.id))
        connect.commit()

    def delete_from_order(self, book_id):
        connect = sqlite3.connect(self.Database)
        cursor = connect.cursor()
        order_id = cursor.execute("select ORDER_ID from _ORDER where BOOK_ID = {} and USER_ID = {}; ".format(
            book_id, self.id)).fetchone()
        cursor.execute("delete from _ORDER where ORDER_ID = {};".format(order_id[0]))
        connect.commit()

    def set_email(self, e_mail):
        connect = sqlite3.connect(self.Database)
        cursor = connect.cursor()
        cursor.execute("update USER set E_MAIL = \"{}\", where USER_ID = {};".format(e_mail, self.id))
        connect.commit()


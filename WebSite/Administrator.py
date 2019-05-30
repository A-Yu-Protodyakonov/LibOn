#from interface import Interface, implements
import sqlite3, os
from SystemMember import SystemMember
from Book import Book
import sqlite3
import os


class Administrator(SystemMember):
    id, email, password = None, None, None
    Database = os.path.join(os.path.dirname(__file__), 'PT.db')

    def __init__(self, id_member, name, lastName, email, password):
        super(Administrator, self).__init__(name, lastName)
        self.id = id_member
        self.email = email
        self.password = password

    def add_book(self, new_book: Book):
        connect = sqlite3.connect(self.Database)
        cursor = connect.cursor()
        rubric_id = cursor.execute("select RUBRIC_ID from RUBRIC where RUBRIC_NAME = \"{}\";".format(
            new_book.rubric_name)).fetchone()
        cursor.execute("INSERT INTO BOOK (BOOK_NAME, AUTHOR, RENTAL_TIME, BOOK_TYPE, RUBRIC_ID) VALUES (\"{}\", \"{}\","
                       "{},{},{});".format(new_book.element_name, new_book.Author, new_book.rentalTime, new_book.type,
                                           rubric_id[0]))
        cursor.execute("insert into BOOK_ADMINISTRATOR values ({}, {});".format(new_book.id, self.id))
        connect.commit()

    def delete_book(self, book: Book):
        connect = sqlite3.connect(self.Database)
        cursor = connect.cursor()
        cursor.execute("delete from BOOK where BOOK_ID = {};".format(book.id))
        connect.commit()

    def change_book(self, book):
        self.change(book)

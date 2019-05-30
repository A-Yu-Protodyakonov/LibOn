import  os
import sqlite3


class Rubric:
    rubric_name = None

    def __init__(self, name):
        Rubric.add_rubric(name)
        self.rubric_name = name

    def set_rubric(self, name):
        self.rubric_name = name

    def get_rubric(self):
        return self.rubric_name

    @staticmethod
    def get_database():
        return os.path.join(os.path.dirname(__file__), 'PT.db')

    @staticmethod
    def add_rubric(name):
        connect = sqlite3.connect(Rubric.get_database())
        cursor = connect.cursor()
        rubric_id = cursor.execute("select RUBRIC_ID from RUBRIC where RUBRIC_NAME = \"{}\";".format(
            name)).fetchone()
        if rubric_id is None:
            cursor.execute("insert into RUBRIC (RUBRIC_NAME) values (\"{}\");".format(name))
            connect.commit()

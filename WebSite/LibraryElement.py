#from interface import Interface, implements
from Rubric import Rubric


class LibraryElement(Rubric):
    element_name = None

    def __init__(self, name, rubric):
        super(LibraryElement, self).__init__(rubric)
        self.element_name = name

    def set_element_name(self, name):
        self.element_name = name

    def get_element_name(self):
        return self.element_name
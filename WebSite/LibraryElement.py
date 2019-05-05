from interface import Interface, implements
from Rubric import Rubric


class LibraryElement(Rubric):
    element_name = None

    def set_element_name(self, name):
        self.element_name = name

    def get_element_name(self):
        return selff.element_name
from interface import Interface, implements


class LibraryElement(Interface):
    element_name = None

    def set_element_name(self, name):
        self.element_name = name

    def get_elenemt_name(self):
        return self.element_name

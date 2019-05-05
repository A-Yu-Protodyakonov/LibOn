from interface import Interface, implements

class Rubric(Interface):
    rubric_name = None

    def set_rubric(self, name):
        self.rubric_name = name

    def get_rubric(self):
        return self.rubric_name
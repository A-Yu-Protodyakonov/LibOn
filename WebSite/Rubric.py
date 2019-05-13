

class Rubric:
    rubric_name = None

    def __init__(self, name):
        self.rubric_name = name

    def set_rubric(self, name):
        self.rubric_name = name

    def get_rubric(self):
        return self.rubric_name


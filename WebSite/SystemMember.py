#from interface import Interface, implements


class SystemMember:
    memberName, memberLastname = None, None

    def __init__(self, name, lastname):
        self.memberName = name.title()
        self.memberLastname = lastname.title()

    def set_name(self, name):
        self.memberName = name

    def set_last_name(self, Lastname):
        self.memberLastname = Lastname

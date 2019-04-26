from interface import Interface, implements


class SystemMember(Interface):
    memberName, memberLastname, location = None, None, None

    def set_name(self, name):
        self.memberName = name

    def set_last_name(self, Lastname):
        self.memberLastname = Lastname

    def location(self, location):
        self.location = location

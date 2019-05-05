from interface import Interface, implements


class SystemMember(Interface):
    memberName, memberLastname = None, None

    def set_name(self, name):
        self.memberName = name

    def set_last_name(self, Lastname):
        self.memberLastname = Lastname
from Book import Book
from Administrator import Administrator
from User import User


class Test:

    def start(self):
        book = Book(1, "Миша хороший человек", "Фантастика", "Vfvrf_Pfrb", 30, 1)
        administrator = Administrator(1, "Александр", "Протодьяконов", "123@mail.ru", "Pa$$w0rd")
        administrator.delete_book(book)


if __name__ == "__main__":
    test = Test()
    test.start()
    pass

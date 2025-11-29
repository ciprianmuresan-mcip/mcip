import pickle
from pdoc import pdoc
from src.domain.domain import Book

class BookError(Exception):
    pass

class DuplicateIDError(BookError):
    pass

class RepositoryIterator:
    """

    """
    def __init__(self, elements):
        """

        :param elements:
        """
        self._elements = elements
        self.__pos = -1

    def __iter__(self):
        """

        :return:
        """
        return self

    def __next__(self):
        """

        :return:
        """
        self.__pos += 1
        if self.__pos == len(self._elements):
            raise StopIteration()

        return self._elements[self.__pos]

class MemoryRepository:
    """

    """
    def __init__(self):
        """

        """
        self._data = {}

    def store(self, book: Book):
        """
        :param book:
        :return:
        """
        if book.isbn in self._data:
            raise DuplicateIDError("Duplicate Book ID")
        self._data[book.isbn] = book

    def display_books(self)->list[Book]:
        """

        :return:
        """
        return list(self._data.values())

    def delete_by_isbn(self, isbn: str):
        """

        :param isbn:
        :return:
        """
        if isbn in self._data:
            del self._data[isbn]

    def __len__(self):
        """

        :return:
        """
        return len(self._data)

    def __iter__(self):
        """

        :return:
        """
        return RepositoryIterator(list(self._data.values()))


class BinaryFileRepository(MemoryRepository):
    """

    """
    def __init__(self, filename: str = "books.bin"):
        """

        :param filename:
        """
        super().__init__()
        self._filename = filename
        self.__load_file()

    def store(self, book: Book):
        """

        :param book:
        :return:
        """
        if book.isbn in self._data:
            raise DuplicateIDError
        super().store(book)
        self.__save_file()

    def delete_by_isbn(self, isbn: str):
        """

        :param isbn:
        :return:
        """
        super().delete_by_isbn(isbn)
        self.__save_file()

    def __save_file(self):
        """

        :return:
        """
        # noinspection PyBroadException
        try:
            fout = open(self._filename, "wb")
            pickle.dump(self._data, fout)
            fout.close()
        except Exception:
            pass

    def __load_file(self):
        """

        :return:
        """
        try:
            fin = open(self._filename, "rb")
            self._data = pickle.load(fin)
            fin.close()
        except FileNotFoundError:
            self._data = {}

class TextFileRepository(MemoryRepository):
    """

    """
    def __init__(self, filename: str = "books.txt"):
        """

        :param filename:
        """
        super().__init__()
        self._filename = filename
        self.__load_file()

    def store(self, book: Book):
        """

        :param book:
        :return:
        """
        if book.isbn in self._data:
            raise DuplicateIDError
        self._data[book.isbn] = book
        self.__save_file()

    def delete_by_isbn(self, isbn: str):
        """

        :param isbn:
        :return:
        """
        super().delete_by_isbn(isbn)
        self.__save_file()

    def __load_file(self):
        """

        :return:
        """
        try:
            fin = open(self._filename, "r")
        except FileNotFoundError:
            return
        self._data = {}
        for line in fin:
            part = line.strip().split(" ")
            if len(part) != 3:
                continue
            isbn , title, author = part
            self._data[isbn] = Book(isbn, title, author)
        fin.close()

    def __save_file(self):
        """

        :return:
        """
        fout = open(self._filename, "w")
        for book in self._data.values():
            fout.write(str(book.isbn) + " " + str(book.title) + " " + str(book.author) + "\n")
        fout.close()


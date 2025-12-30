import pickle
from src.domain.book_domain import Book


class BookError(Exception):
    pass


class DuplicateIDError(BookError):
    pass


class BookNotFoundError(BookError):
    pass


class RepositoryIterator:
    def __init__(self, elements):
        self._elements = elements
        self.__pos = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.__pos += 1
        if self.__pos == len(self._elements):
            raise StopIteration()
        return self._elements[self.__pos]


class BookMemoryRepository:
    def __init__(self):
        self._data = {}

    def get_book(self, book_id: str) -> Book:
        if book_id not in self._data:
            raise BookNotFoundError(f"Book ID '{book_id}' not found.")
        return self._data[book_id]

    def is_available(self, book_id: str) -> bool:
        if book_id not in self._data:
            raise BookNotFoundError(f"Book ID '{book_id}' not found.")
        return self._data[book_id].get_is_available

    def set_availability(self, book_id: str, is_available: bool):
        if book_id not in self._data:
            raise BookNotFoundError(f"Book ID '{book_id}' not found.")
        self._data[book_id].get_is_available = is_available

    def add_book(self, book: Book):
        if book.get_book_id in self._data:
            raise DuplicateIDError("Duplicate Book ID")
        self._data[book.get_book_id] = book

    def remove_book(self, title: str) -> Book:
        """
        Removes a book by title and returns the removed Book object.
        """
        to_delete_id = None
        deleted_book = None

        for book in self._data.values():
            if title.lower() == book.get_title.lower():
                to_delete_id = book.get_book_id
                deleted_book = book
                break

        if to_delete_id is None:
            raise BookNotFoundError(f"No book with title '{title}' found.")

        del self._data[to_delete_id]
        return deleted_book

    def update_book(self, book_id: str, title: str, author: str):
        if book_id not in self._data:
            raise BookNotFoundError(f"Book ID '{book_id}' not found.")
        book = self._data[book_id]
        book._title = title
        book._author = author

    def display_all_books(self) -> list[Book]:
        return list(self._data.values())

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return RepositoryIterator(list(self._data.values()))


class BookBinaryFileRepository(BookMemoryRepository):
    def __init__(self, filename: str = "books.bin"):
        super().__init__()
        self._filename = filename
        self.__load_file()

    def set_availability(self, book_id: str, is_available: bool):
        super().set_availability(book_id, is_available)
        self.__save_file()

    def add_book(self, book: Book):
        super().add_book(book)
        self.__save_file()

    def remove_book(self, title: str) -> Book:
        deleted_book = super().remove_book(title)
        self.__save_file()
        return deleted_book

    def update_book(self, book_id: str, title: str, author: str):
        super().update_book(book_id, title, author)
        self.__save_file()

    def __save_file(self):
        try:
            with open(self._filename, "wb") as fout:
                pickle.dump(self._data, fout)
        except Exception:
            pass

    def __load_file(self):
        try:
            with open(self._filename, "rb") as fin:
                self._data = pickle.load(fin)
        except FileNotFoundError:
            self._data = {}


class BookTextFileRepository(BookMemoryRepository):
    def __init__(self, filename: str = "books.txt"):
        super().__init__()
        self._filename = filename
        self.__load_file()

    def set_availability(self, book_id: str, is_available: bool):
        super().set_availability(book_id, is_available)
        self.__save_file()

    def add_book(self, book: Book):
        super().add_book(book)
        self.__save_file()

    def remove_book(self, title: str) -> Book:
        deleted_book = super().remove_book(title)
        self.__save_file()
        return deleted_book

    def update_book(self, book_id: str, title: str, author: str):
        super().update_book(book_id, title, author)
        self.__save_file()

    def __load_file(self):
        try:
            fin = open(self._filename, "r")
        except FileNotFoundError:
            return
        self._data = {}
        for line in fin:
            part = line.strip().split(", ")
            if len(part) < 3:
                continue
            book_id, title, author = part[0:3]
            is_available = True
            if len(part) > 3 and part[3] == '0':
                is_available = False
            self._data[book_id] = Book(book_id, title, author, is_available)
        fin.close()

    def __save_file(self):
        fout = open(self._filename, "w")
        for book in self._data.values():
            avail_str = "1" if book.get_is_available else "0"
            fout.write(f"{book.get_book_id}, {book.get_title}, {book.get_author}, {avail_str}\n")
        fout.close()
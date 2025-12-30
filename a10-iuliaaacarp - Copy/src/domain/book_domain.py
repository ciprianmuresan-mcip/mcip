class Book:
    """
    Represents a book in the library
    """
    def __init__(self, book_id: str, title: str, author: str, is_available: bool):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._is_available = is_available

    @property
    def get_book_id(self):
        return self._book_id

    @property
    def get_title(self):
        return self._title

    @property
    def get_author(self):
        return self._author

    @property
    def get_is_available(self):
        return self._is_available

    @get_is_available.setter
    def get_is_available(self, value: bool):
        self._is_available = value

    def __str__(self):
        return f"ID: {self.get_book_id}| {self.get_title} by {self.get_author}"

    def __repr__(self):
        return self.__str__()
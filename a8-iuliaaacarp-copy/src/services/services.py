from src.domain.domain import Book

class UndoAddBook(Book):
    def __init__(self, repo, isbn):
        self._repo = repo
        self._isbn = isbn


    def undo(self):
        self._repo.delete_by_isbn(self.isbn)

class UndoRemoveBook(Book):
    def __init__(self, repo, books_remove_isbn):
        self.repo = repo
        self.books_remove_isbn = books_remove_isbn
    def undo(self):
        for book in self.books_remove_isbn:
            self.repo.store(book)


class BookService:
    def __init__(self, repository):
        self._repo = repository
        self._history = []

    def add_book(self, isbn: str, title: str, author: str):
        book = Book(isbn, title, author)
        self._repo.store(book)
        self._history.append(UndoAddBook(self._repo, isbn))

    def list_books(self):
        return list(self._repo)

    def remove_book_starting_with_word(self, word: str):
        books_remove_isbn = []
        for book in self._repo:
            if book.title.lower().startswith(word.lower()):
                books_remove_isbn.append(book.isbn)
        for isbn in books_remove_isbn:
            self._repo.delete_by_isbn(isbn)
            self._history.append(UndoRemoveBook(self._repo, books_remove_isbn))

    def undo(self):
        if not self._history:
            raise Exception("No operations to undo")

        self._history.pop().undo()



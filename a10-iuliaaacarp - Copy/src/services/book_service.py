import random
from src.domain.book_domain import Book
from src.services.undo_service import UndoService, Operation, FunctionCall, CascadedOperation
from src.services.rental_service import RentalService


class BookService:
    def __init__(self, book_repo, undo_service: UndoService, rental_service: RentalService):
        self._book_repo = book_repo
        self._undo_service = undo_service
        self._rental_service = rental_service

    def get_book(self, book_id):
        return self._book_repo.get_book(book_id)

    @staticmethod
    def generate_book_id():
        return str(random.randint(1000, 9999))

    def is_book_available(self, book_id):
        return self._book_repo.is_available(book_id)

    def set_book_availability(self, book_id, is_available):
        self._book_repo.set_availability(book_id, is_available)

    def add_book(self, book_id, book_title, book_author):
        book = Book(book_id, book_title, book_author, True)
        self._book_repo.add_book(book)

        undo_function = FunctionCall(self._book_repo.remove_book, book_title)
        redo_function = FunctionCall(self._book_repo.add_book, book)

        self._undo_service.record(Operation(undo_function, redo_function))

    def remove_book(self, book_title):
        book_id = self.search_title_id(book_title)

        if book_id is None:
            pass
        rentals_to_remove = []
        if self._rental_service:
            rentals_to_remove = self._rental_service.get_rentals_by_book_id(book_id)
            self._rental_service.delete_rentals_for_book(book_id)

        deleted_book = self._book_repo.remove_book(book_title)

        all_ops = []

        for rental in rentals_to_remove:
            undo_rental = FunctionCall(self._rental_service.add_rental_object, rental)
            redo_rental = FunctionCall(self._rental_service.delete_rental_by_id, rental.get_rental_id)
            all_ops.append(Operation(undo_rental, redo_rental))

        undo_book = FunctionCall(self._book_repo.add_book, deleted_book)
        redo_book = FunctionCall(self._book_repo.remove_book, book_title)
        all_ops.append(Operation(undo_book, redo_book))

        self._undo_service.record(CascadedOperation(*reversed(all_ops)))

    def update_book(self, book_id, book_title, book_author):
        original_book = self._book_repo.get_book(book_id)
        original_title = original_book.get_title
        original_author = original_book.get_author

        self._book_repo.update_book(book_id, book_title, book_author)

        undo_function = FunctionCall(self._book_repo.update_book, book_id, original_title, original_author)
        redo_function = FunctionCall(self._book_repo.update_book, book_id, book_title, book_author)

        self._undo_service.record(Operation(undo_function, redo_function))

    def display_all_books(self):
        return list(self._book_repo)

    def search_book_id(self, book_id):
        search = []
        book_id_str = str(book_id).lower()
        for book in self._book_repo:
            if book_id_str in str(book.get_book_id).lower():
                search.append(book)
        return search

    def search_book_title(self, book_title):
        search = []
        book_title_str = str(book_title).lower()
        for book in self._book_repo:
            if book_title_str in book.get_title.lower():
                search.append(book)
        return search

    def search_book_author(self, book_author):
        search = []
        book_author_str = str(book_author).lower()
        for book in self._book_repo:
            if book_author_str in book.get_author.lower():
                search.append(book)
        return search

    def search_title_id(self, book_title):
        book_title_str = str(book_title).lower()
        for book in self._book_repo:
            if book_title_str == book.get_title.lower():
                return book.get_book_id
        return None

    def search_author_id(self, book_id):
        book_id_str = str(book_id).lower()
        for book in self._book_repo:
            if book_id_str == book.get_book_id.lower():
                return book.get_author
        return None



    @property
    def book_repo(self):
        return self._book_repo
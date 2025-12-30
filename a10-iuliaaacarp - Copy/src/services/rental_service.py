# rental_service.py
import random
from src.domain.rental_domain import Rental
from src.services.undo_service import UndoService, Operation, FunctionCall, CascadedOperation

class RentalError(Exception):
    pass

class RentalService:
    def __init__(self, rental_repo, book_service, client_service, undo_service: UndoService):
        self._rental_repo = rental_repo
        self._book_service = book_service
        self._client_service = client_service
        self._undo_service = undo_service

    @staticmethod
    def generate_rental_id():
        return random.randint(10000, 99999)

    def get_rental(self, rental_id):
        return self._rental_repo.get_rental(rental_id)

    def get_all_rentals(self):
        return list(self._rental_repo)

    def rent_book(self, rental_id, client_id, book_title, rented_date, returned_date):
        book_id = self._book_service.search_title_id(book_title)
        if book_id is None:
            raise RentalError("Book not found")
        if not self._book_service.is_book_available(book_id):
            raise RentalError("Book not available")
        rental = Rental(rental_id, book_id, client_id, rented_date, returned_date)
        self._rental_repo.add_rental(rental)
        self._book_service.set_book_availability(book_id, False)
        rental_operation = Operation(FunctionCall(self._rental_repo.remove_rental, rental_id),
                                     FunctionCall(self._rental_repo.add_rental, rental))
        book_operation = Operation(FunctionCall(self._book_service.set_book_availability, book_id, True),
                                   FunctionCall(self._book_service.set_book_availability, book_id, False))
        self._undo_service.record(CascadedOperation(rental_operation, book_operation))

    def return_book(self, book_title):
        book_id = self._book_service.search_title_id(book_title)
        if book_id is None:
            raise RentalError("Book not found.")
        active_rental = None
        for rental in self._rental_repo:
            if rental.get_book_id == book_id and not rental.get_returned_date:
                active_rental = rental
                break
        if active_rental is None:
            raise RentalError(f"Book '{book_title}' is not currently rented.")
        rental_id = active_rental.get_rental_id
        original_returned_date = active_rental.get_returned_date
        self._rental_repo.return_book(rental_id)
        self._book_service.set_book_availability(book_id, True)
        op_rental = Operation(
            FunctionCall(self._rental_repo.reset_returned_date, rental_id, original_returned_date),
            FunctionCall(self._rental_repo.return_book, rental_id)
        )
        op_book_status = Operation(
            FunctionCall(self._book_service.set_book_availability, book_id, False),
            FunctionCall(self._book_service.set_book_availability, book_id, True)
        )
        self._undo_service.record(CascadedOperation(op_rental, op_book_status))

    def get_rentals_by_book_id(self, book_id):
        return [r for r in self._rental_repo if r.get_book_id == book_id]

    def delete_rentals_for_book(self, book_id):
        rentals_to_delete = self.get_rentals_by_book_id(book_id)
        for rental in rentals_to_delete:
            self._rental_repo.remove_rental(rental.get_rental_id)

    def add_rental_object(self, rental_object):
        self._rental_repo.add_rental(rental_object)

    def delete_rental_by_id(self, rental_id):
        self._rental_repo.remove_rental(rental_id)

    def delete_rental_book(self, book_id):
        for rental in self._rental_repo:
            if rental.get_book_id == book_id:
                self._rental_repo.remove_rental(rental.get_rental_id)

    def list_rentals(self):
        rentals_display = []
        for rental in self._rental_repo:
            rentals_display.append(
                f"Rental ID: {rental.get_rental_id} | Book: {rental.get_book_id} | Client: {rental.get_client_id} | Rented: {rental.get_rented_date} | Returned: {rental.get_returned_date or 'Not returned'}"
            )
        return rentals_display
import pickle
from src.domain.rental_domain import Rental

class RentalError(Exception):
    pass

class DuplicateIDError(RentalError):
    pass

class RentalNotFoundError(RentalError):
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

class RentalMemoryRepository:
    def __init__(self):
        self._data = {}

    def add_rental(self, rental: Rental):
        if rental.get_rental_id in self._data:
            raise DuplicateIDError("Duplicate Rental ID")
        for r in self._data.values():
            if r.get_book_id == rental.get_book_id:
                raise DuplicateIDError("Book is already rented")
        self._data[rental.get_rental_id] = rental

    def return_book(self, rental_id):
        if rental_id in self._data:
            del self._data[rental_id]

    def remove_rental(self, rental_id):
        if rental_id not in self._data:
            raise RentalNotFoundError("Rental ID not found")
        del self._data[rental_id]

    def reset_returned_date(self, rental_id, original_date):
        if rental_id not in self._data:
            raise RentalNotFoundError("Rental ID not found")

        self._data[rental_id].returned_date = original_date

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return RepositoryIterator(list(self._data.values()))

class RentalBinaryFileRepository(RentalMemoryRepository):
    def __init__(self, filename="rentals.bin"):
        super().__init__()
        self._filename = filename
        self.__load_file()

    def add_rental(self, rental: Rental):
        super().add_rental(rental)
        self.__save_file()

    def return_book(self, rental_id):
        super().return_book(rental_id)
        self.__save_file()

    def __save_file(self):
        try:
            with open(self._filename, "wb") as f:
                pickle.dump(self._data, f)
        except Exception:
            pass

    def __load_file(self):
        try:
            with open(self._filename, "rb") as f:
                self._data = pickle.load(f)
        except FileNotFoundError:
            self._data = {}

class RentalTextFileRepository(RentalMemoryRepository):
    def __init__(self, filename="rentals.txt"):
        super().__init__()
        self._filename = filename
        self.__load_file()

    def add_rental(self, rental: Rental):
        super().add_rental(rental)
        self.__save_file()

    def return_book(self, rental_id):
        super().return_book(rental_id)
        self.__save_file()

    def __load_file(self):
        try:
            with open(self._filename, "r") as f:
                self._data = {}
                for line in f:
                    parts = line.strip().split(", ")
                    if len(parts) != 5:
                        continue
                    rental_id, book_id, client_id, rented_date, returned_date = parts
                    self._data[rental_id] = Rental(rental_id, book_id, client_id, rented_date, returned_date)
        except FileNotFoundError:
            self._data = {}

    def __save_file(self):
        with open(self._filename, "w") as f:
            for rental in self._data.values():
                f.write(f"{rental.get_rental_id}, {rental.get_book_id}, {rental.get_client_id}, {rental.get_rented_date}, {rental.get_returned_date}\n")

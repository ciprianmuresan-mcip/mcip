class Rental:
    def __init__(self, rental_id: str, book_id: str, client_id: str, rented_date: str, returned_date: str):
        self._rental_id = rental_id
        self._book_id = book_id
        self._client_id = client_id
        self._rented_date = rented_date
        self._returned_date = returned_date

    @property
    def get_rental_id(self):
        return self._rental_id

    @property
    def get_book_id(self):
        return self._book_id

    @property
    def get_client_id(self):
        return self._client_id

    @property
    def get_rented_date(self):
        return self._rented_date

    @property
    def get_returned_date(self):
        return self._returned_date

    def __str__(self):
        return f"ID:{self.get_rental_id} | {self.get_book_id} | {self.get_client_id} | {self.get_rented_date} {self.get_returned_date}\n"

    def __repr__(self):
        return self.__str__()

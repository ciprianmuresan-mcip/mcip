from collections import Counter
from datetime import datetime

from src.domain.statistics_domain import RentalStats
from src.domain.rental_domain import Rental

from src.services.book_service import BookService
from src.services.client_service import ClientService
from src.services.rental_service import RentalService

from typing import List, Tuple, Dict

class StatisticsService:
    def __init__(self, rental_service: RentalService, book_service: BookService, client_service: ClientService):
        self._rental_service = rental_service
        self._book_service = book_service
        self._client_service = client_service

    @staticmethod
    def _calculate_days_rented(rental):
        rented_date = datetime.strptime(rental.get_rented_date, "%Y-%m-%d")
        if rental.get_returned_date == "Not returned" or rental.get_returned_date == "":
            returned_date = datetime.now()
        else:
            returned_date = datetime.strptime(rental.get_returned_date, "%Y-%m-%d")

        time_span = returned_date - rented_date
        return time_span.days

    def get_most_rented_books(self):
        rentals = self._rental_service.get_all_rentals()

        counts = {}
        for rental in rentals:
            book_id = rental.get_book_id
            counts[book_id] = counts.get(book_id, 0) + 1

        result = []
        for book_id, count in counts.items():
            book = self._book_service.get_book(book_id)
            result.append(RentalStats(book.get_title, count, book.get_author))

        result.sort(key=lambda x: x.value, reverse=True)
        return result

    def get_most_active_clients(self):
        rentals = self._rental_service.get_all_rentals()
        client_days = {}

        for rental in rentals:
            returned = rental.get_returned_date
            if returned and returned != "Not returned":
                start = datetime.fromisoformat(rental.get_rented_date)
                end = datetime.fromisoformat(rental.get_returned_date)
                days = (end - start).days

                client_days[rental.get_client_id] = (
                        client_days.get(rental.get_client_id, 0) + days
                )

        result = []
        for client_id, days in client_days.items():
            client = self._client_service.get_client(client_id)
            result.append(RentalStats(client.get_client_name, days))

        result.sort(key=lambda x: x.value, reverse=True)
        return result

    def get_most_rented_authors(self):
        rentals = self._rental_service.get_all_rentals()
        author_counts = {}

        for rental in rentals:
            book = self._book_service.get_book(rental.get_book_id)
            author = book.get_author
            author_counts[author] = author_counts.get(author, 0) + 1

        result = [
            RentalStats(author, count)
            for author, count in author_counts.items()
        ]

        result.sort(key=lambda x: x.value, reverse=True)
        return result



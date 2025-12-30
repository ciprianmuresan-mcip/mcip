from datetime import date
import os

from src.repository.change_repository import RepositoryChange
from src.services.book_service import BookService
from src.services.client_service import ClientService
from src.services.rental_service import RentalService
from src.services.undo_service import UndoService
from src.services.statistics_service import StatisticsService


class UserInterface:
    def __init__(self, book_service: BookService, client_service: ClientService, rental_service: RentalService,
                 undo_service: UndoService, statistics_service: StatisticsService):
        self.running = True
        self._book_service = book_service
        self._client_service = client_service
        self._rental_service = rental_service
        self._undo_service = undo_service
        self._statistics_service = statistics_service

    @staticmethod
    def display_menu():
        print("\n--------Welcome to the library!--------")
        print(" 1. Manage books/clients. Type B or C and then a command from below:")
        print("     a. Add")
        print("     b. Remove")
        print("     c. Update")
        print("     d. List all")
        print(" 2. Rent a book")
        print(" 3. Return a book")
        print(" 4. Search for a book")
        print(" 5. Search for a client")
        print(" 6. List all rentals")
        print(" u. Undo the last operation")
        print(" r. Redo the last operation")
        print(" x. Exit")
        print("\n--------Statistics--------")
        print(" s1. Most rented books")
        print(" s2. Most active clients")
        print(" s3. Most rented authors")

    @staticmethod
    def user_run():
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        settings_path = os.path.join(base_dir, "repository", "settings.properties")

        if not os.path.exists(settings_path):
            settings_path = "settings.properties"

        try:
            repo_manager = RepositoryChange(settings_path)

            book_repo = repo_manager.create_repo_book()
            client_repo = repo_manager.create_repo_client()
            rental_repo = repo_manager.create_repo_rental()

            undo_service = UndoService()

            book_service = BookService(book_repo, undo_service, None)
            client_service = ClientService(client_repo, undo_service)
            rental_service = RentalService(rental_repo, book_service, client_service, undo_service)

            statistics_service = StatisticsService(rental_service, book_service, client_service)

            book_service._rental_service = rental_service

            return UserInterface(book_service, client_service, rental_service, undo_service, statistics_service)

        except Exception as e:
            print(f"Error initializing repositories or services: {e}")
            return None

    def run(self):
        if self._book_service is None:
            print("Initialization failed.")
            return

        options = {
            "1Ba": self.add_book, "1Bb": self.remove_book, "1Bc": self.update_book, "1Bd": self.display_all_books,
            "1Ca": self.add_client, "1Cb": self.remove_client, "1Cc": self.update_client,
            "1Cd": self.display_all_clients,
            "2": self.rent_book, "3": self.return_book, "4": self.search_book, "5": self.search_client,
            "6": self.display_all_rentals, "u": self.undo_operation, "r": self.redo_operation,
            "s1": self.most_rented_books, "s2": self.most_active_clients, "s3": self.most_rented_authors
        }

        while self.running:
            self.display_menu()
            choice = input("Please enter your choice: ")
            if choice in options:
                try:
                    options[choice]()
                except Exception as e:
                    print(f"Operation failed: {e}")
            elif choice == 'x':
                print("Exiting the application. Goodbye!")
                self.running = False
            else:
                print("Invalid choice. Please try again.")

    def undo_operation(self):
        try:
            self._undo_service.undo()
            print("Undoing operation finished.")
        except Exception as e:
            print(e)

    def redo_operation(self):
        try:
            self._undo_service.redo()
            print("Redoing operation finished.")
        except Exception as e:
            print(e)

    def most_rented_books(self):
        most_rented = self._statistics_service.get_most_rented_books()
        top = 0
        print("----Most rented books----")
        for r in most_rented:
            if top < 5:
                print(f"Title: {r.name}: | No. of rentals: {r.value}")
            top += 1

    def most_active_clients(self):
        most_active = self._statistics_service.get_most_active_clients()
        top = 0
        print("----Most active clients----")
        for r in most_active:
            if top < 5:
                print(f"Name: {r.name}: | Days rented: {r.value}")
            top += 1

    def most_rented_authors(self):
        most_rented = self._statistics_service.get_most_rented_authors()
        top = 0
        print("----Most rented authors----")
        for r in most_rented:
            if top < 5:
                print(f"Name: {r.name}: | No. of rentals: {r.value}")
            top += 1

    def add_book(self):
        book_id = self._book_service.generate_book_id()
        book_title = input("Please enter the book title: ")
        book_author = input("Please enter the book author: ")
        self._book_service.add_book(book_id, book_title, book_author)
        print(f"Book '{book_title}' by {book_author} added successfully.")

    def remove_book(self):
        book_title = input("Please enter the book title you want to remove: ")
        self._book_service.remove_book(book_title)
        print(f"Book '{book_title}' removed successfully.")

    def update_book(self):
        book_id = input("Please enter the book id you want to update: ")
        book_title = input("Please enter the new book title: ")
        book_author = input("Please enter the new book author: ")
        self._book_service.update_book(book_id, book_title, book_author)
        print(f"Book '{book_title}' updated successfully.")

    def display_all_books(self):
        books = self._book_service.display_all_books()
        for book in books:
            print(book)

    def rent_book(self):
        try:
            rental_id = str(self._rental_service.generate_rental_id())

            client_id = input("Please enter the client id: ")
            # FIX: Get client name by ID using helper
            try:
                client_name = self._client_service.get_client_name_by_id(client_id)
            except Exception:
                print("Client ID not found.")
                return

            book_title = input("Please enter the book title you want to rent: ")
            rented_date = str(date.today())
            returned_date = ""  # Empty for now

            self._rental_service.rent_book(rental_id, client_id, book_title, rented_date, returned_date)
            print(f"Book '{book_title}' rented to '{client_name}' ('{client_id}') successfully.")
        except Exception as e:
            print(f"Error renting book: {e}")

    def return_book(self):
        book_title = input("Please enter the book title you want to return: ")
        self._rental_service.return_book(book_title)
        print(f"Book '{book_title}' returned successfully.")

    def display_all_rentals(self):
        rentals = self._rental_service.list_rentals()
        if not rentals:
            print("No rentals found.")
            return
        for rental_str in rentals:
            print(rental_str)

    def search_book(self):
        option = input("Search by 'id', 'title', or 'author': ").lower()
        if option == "id":
            book_id = input("Enter the book id: ")
            results = self._book_service.search_book_id(book_id)
        elif option == "title":
            book_title = input("Enter the book title: ")
            results = self._book_service.search_book_title(book_title)
        elif option == "author":
            book_author = input("Enter the book author: ")
            results = self._book_service.search_book_author(book_author)
        else:
            print("Invalid option")
            return
        for r in results:
            print(r)

    def add_client(self):
        client_id = self._client_service.generate_client_id()
        client_name = input("Please enter the client name: ")
        self._client_service.add_client(client_id, client_name)
        print(f"Client '{client_name}' added successfully.")

    def remove_client(self):
        client_id = input("Please enter the client id to remove: ")
        self._client_service.remove_client(client_id)
        print(f"Client '{client_id}' removed successfully.")

    def update_client(self):
        client_id = input("Please enter the client id to update: ")
        client_name = input("Please enter the new client name: ")
        self._client_service.update_client(client_id, client_name)
        print(f"Client '{client_name}' updated successfully.")

    def display_all_clients(self):
        clients = self._client_service.display_all_clients()
        for client in clients:
            print(client)

    def search_client(self):
        option = input("Search by 'id' or 'name': ").lower()
        if option == "id":
            client_id = input("Enter the client id: ")
            results = self._client_service.search_client_id(client_id)
        elif option == "name":
            client_name = input("Enter the client name: ")
            results = self._client_service.search_client_name(client_name)
        else:
            print("Invalid option")
            return
        for r in results:
            print(r)


if __name__ == "__main__":
    ui = UserInterface.user_run()
    if ui:
        ui.run()
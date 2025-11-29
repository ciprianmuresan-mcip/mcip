# User interface

from texttable import Texttable

from src.repository.repository import TextFileRepository, BinaryFileRepository
from src.services.services import BookService

class UserInterface:
    def __init__(self, service: BookService) -> None:
        self.running = True
        self._service = service

    @staticmethod
    def display_menu():
        t = Texttable()
        t.add_row(["", "Books Management Menu"])
        t.add_row(["1", "Add a book"])
        t.add_row(["2", "Display all books"])
        t.add_row(["3", "Filter books by title"])
        t.add_row(["u", "Undo last operation"])
        t.add_row(["x", "Exit"])
        print(t.draw())

    @staticmethod
    def get_user_choice():
        choice = input("Please enter your choice (1-4): ")
        return choice

    def add_book(self):
        isbn = input("Please enter ISBN: ")
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        self._service.add_book(isbn, title, author)
        print(f"Book '{title}' by {author} added successfully.")

    def display_all_books(self):
        print("Displaying all books...")
        all_books = self._service.list_books()
        for book in all_books:
            print(book)

    def filter_books_by_title(self):
        word = input("Enter word to filter by: ")
        print(f"Filtering books by removing the ones starting with: {word}")
        # Placeholder for filtering books logic
        self._service.remove_book_starting_with_word(word)


    """""
    def undo_operation(self):
        print("Undoing last operation...")
        self._service.undo()
        """

    def run(self):
        options = {"1": self.add_book, "2": self.display_all_books, "3": self.filter_books_by_title, "u": self._service.undo}
        while self.running:
            self.display_menu()
            choice = self.get_user_choice()
            if choice in options:
                try:
                    options[choice]()
                except Exception as e:
                    print(e)
            elif choice == 'x':
                print("Exiting the application. Goodbye!")
                self.running = False
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    repo1 = TextFileRepository("books.txt")
    repo2 = BinaryFileRepository("books.bin")
    service = BookService(repo1)
    user = UserInterface(service)
    user.run()

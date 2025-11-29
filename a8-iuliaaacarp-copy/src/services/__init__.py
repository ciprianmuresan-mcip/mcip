
class BookService:
    def __init__(self):
        self.books = []
        self.history = []

    def add_book(self, title: str, author: str):
        book = Book(title, author)
        self.books.append(book)
        self.history.append(('add', book))

    def get_all_books(self):
        return self.books

    def filter_books_by_title(self, title: str):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def undo_last_operation(self):
        if not self.history:
            return "No operations to undo."

        last_action, book = self.history.pop()
        if last_action == 'add':
            self.books.remove(book)
            return f"Undid addition of book: {book}"

        return "Unknown operation."

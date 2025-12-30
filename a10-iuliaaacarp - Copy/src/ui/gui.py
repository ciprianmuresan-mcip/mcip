import tkinter as tk
import os
from datetime import date
from time import sleep
from tkinter import ttk, messagebox, simpledialog

from src.repository.change_repository import RepositoryChange
from src.services.book_service import BookService
from src.services.client_service import ClientService
from src.services.rental_service import RentalService
from src.services.undo_service import UndoService
from src.services.statistics_service import StatisticsService

class GUI:
    def __init__(self, main_window, book_service, client_service, rental_service, undo_service, statistics_service):
        self.main_window = main_window
        main_window.title("Library Management System")
        main_window.geometry("800x600")
        self._book_service = book_service
        self._client_service = client_service
        self._rental_service = rental_service
        self._undo_service = undo_service
        self._statistics_service = statistics_service
        self.create_action_bar(main_window)
        self.notebook = ttk.Notebook(main_window)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")
        self.create_management_tab()
        self.create_rental_tab()
        self.create_search_tab()
        self.create_statistics_tab()
        self.update_listbox(self.book_listbox, self._book_service.display_all_books())

    @staticmethod
    def _user_run_init():
        """
        Replicates the logic from ui.user_run() for service initialization.
        """
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            settings_path = os.path.join(base_dir, "repository", "settings.properties")

            if not os.path.exists(settings_path):
                settings_path = "settings.properties"

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

            return book_service, client_service, rental_service, undo_service, statistics_service

        except Exception as e:
            messagebox.showerror("Initialization Error", f"Error initializing repositories or services: {e}")
            return None, None, None, None, None

    def create_management_tab(self):
        management_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(management_tab, text="Book_Management")
        # select books / clients
        ttk.Label(management_tab, text="Select entity to manage:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entity_var = tk.StringVar(value="Book")
        entity_selector = ttk.Combobox(management_tab, textvariable=self.entity_var,
                                       values=["Book", "Client"], state="readonly", width=10)
        entity_selector.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        entity_selector.bind("<<ComboboxSelected>>", self.on_entity_change)

        # add, remove update
        button_frame = ttk.Frame(management_tab)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="w")
        ttk.Button(button_frame, text="Add", command=self.add_something).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Remove", command=self.remove_something).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Update", command=self.update_something).pack(side="left", padx=10)

        # listbox to display entities
        list_frame = ttk.Frame(management_tab)
        list_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        management_tab.grid_rowconfigure(2, weight=1)
        management_tab.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.book_listbox = tk.Listbox(list_frame, height=20, width=50, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
        scrollbar.config(command=self.book_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.book_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def create_rental_tab(self):
        rental_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(rental_frame, text="Rentals")
        # renting
        rent_group = ttk.LabelFrame(rental_frame, text="Rent a book", padding=10)
        rent_group.pack(fill="x", pady=10)

        ttk.Label(rent_group, text="Client ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.rent_client_id_entry = ttk.Entry(rent_group, width=30)
        self.rent_client_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(rent_group, text="Book title:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.rent_book_title_entry = ttk.Entry(rent_group, width=30)
        self.rent_book_title_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ttk.Button(rent_group, text="Rent book", command=self.rent_book).grid(row=2, column=1, padx=5, pady=10, sticky="w")
        # returning
        return_group = ttk.LabelFrame(rental_frame, text="Return a book", padding=10)
        return_group.pack(fill="x", pady=10)

        ttk.Label(return_group, text="Book Title:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.return_book_title_entry = ttk.Entry(return_group, width=30)
        self.return_book_title_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ttk.Button(return_group, text="Return book", command=self.return_book).grid(row=1, column=1, padx=5, pady=10, sticky="w")
        # all rentals
        ttk.Button(rental_frame, text="List all rentals", command=self.list_all_rentals).pack(pady=10)

        rental_list_frame = ttk.Frame(rental_frame)
        rental_list_frame.pack(fill="both", expand=True)

        rental_scrollbar = ttk.Scrollbar(rental_list_frame, orient=tk.VERTICAL)
        self.rental_listbox = tk.Listbox(rental_list_frame, height=10, yscrollcommand=rental_scrollbar.set)
        rental_scrollbar.config(command=self.rental_listbox.yview)

        rental_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.rental_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


    def create_search_tab(self):
        search_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(search_frame, text="Search")

        # search for book / client
        ttk.Label(search_frame, text="Search Entity:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_entity_var = tk.StringVar(value="Book")
        search_entity_selector = ttk.Combobox(search_frame, textvariable=self.search_entity_var, values=["Book", "Client"], state="readonly", width=10)
        search_entity_selector.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        search_entity_selector.bind("<<ComboboxSelected>>", self.on_search_entity_change)

        # search by
        ttk.Label(search_frame, text="Search by:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.search_by_var = tk.StringVar(value="id")
        self.search_by_combo = ttk.Combobox(search_frame, textvariable=self.search_by_var, values=["id", "title", "author"], state="readonly", width=10)
        self.search_by_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # search input
        ttk.Label(search_frame, text="Search value:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.search_value_entry = ttk.Entry(search_frame, width=30)
        self.search_value_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        ttk.Button(search_frame, text="Search", command=self.perform_search).grid(row=3, column=1, padx=5, pady=10, sticky="w")

        # results listbox
        search_list_frame = ttk.Frame(search_frame)
        search_list_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        search_frame.grid_rowconfigure(4, weight=1)
        search_frame.grid_columnconfigure(0, weight=1)

        search_scrollbar = ttk.Scrollbar(search_list_frame, orient=tk.VERTICAL)
        self.search_listbox = tk.Listbox(search_list_frame, height=10, yscrollcommand=search_scrollbar.set)
        search_scrollbar.config(command=self.search_listbox.yview)

        search_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.search_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


    def create_statistics_tab(self):
        statistics_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(statistics_frame, text="Statistics")

        ttk.Label(statistics_frame, text="Most rented books (Top 5):", font=('Helvetica', 12, 'bold')).pack(pady=(10, 5))
        self.s1_listbox = self.create_stats_listbox(statistics_frame, self.most_rented_books)

        ttk.Label(statistics_frame, text="Most active clients (Top 5):", font=('Helvetica', 12, 'bold')).pack(pady=(10, 5))
        self.s2_listbox = self.create_stats_listbox(statistics_frame, self.most_active_clients)

        ttk.Label(statistics_frame, text="Most rented authors (Top 5):", font=('Helvetica', 12, 'bold')).pack(pady=(10, 5))
        self.s3_listbox = self.create_stats_listbox(statistics_frame, self.most_rented_authors)

        self.most_rented_books()
        self.most_active_clients()
        self.most_rented_authors()

    @staticmethod
    def create_stats_listbox(parent_frame, refresh_command):
        frame = ttk.Frame(parent_frame)
        frame.pack(fill=tk.X, padx=5, pady=5)
        listbox = tk.Listbox(frame, height=5)
        listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(frame, text="Refresh", command=refresh_command, width=8).pack(side=tk.RIGHT, padx=5)
        return listbox

    def create_action_bar(self, master):
        action_frame = ttk.Frame(master, padding="10")
        action_frame.pack(fill="x")
        ttk.Button(action_frame, text="Undo", command = self.undo_operation).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Redo", command = self.redo_operation).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Exit", command=master.quit).pack(side=tk.RIGHT, padx=5)

    # utility stuff
    @staticmethod
    def update_listbox(listbox, data_list):
        listbox.delete(0, tk.END)
        for item in data_list:
            listbox.insert(tk.END, item)

    def on_entity_change(self, event=None):
        entity = self.entity_var.get()

        if entity == "Book":
            data = self._book_service.display_all_books()
        elif entity == "Client":
            data = self._client_service.display_all_clients()

        self.update_listbox(self.book_listbox, data)

    def on_search_entity_change(self, event=None):
        entity = self.search_entity_var.get()
        if entity == "Book":
            self.search_by_combo['values'] = ["id", "title", "author"]
            self.search_by_var.set("id")
        elif entity == "Client":
            self.search_by_combo['values'] = ["id", "name"]
            self.search_by_var.set("id")

    def add_something(self):
        entity = self.entity_var.get()
        if entity == "Book":
            book_id = self._book_service.generate_book_id()
            title = simpledialog.askstring("Add book", "Enter book title")
            if not title: return
            author = simpledialog.askstring("Add book", "Enter book author")
            if not author: return
            self._book_service.add_book(book_id, title, author)
            messagebox.showinfo("Success!", f"Book {title} was added.")

        elif entity == "Client":
            client_id = self._client_service.generate_client_id()
            name = simpledialog.askstring("Add client", "Enter client name")
            if not name: return
            self._client_service.add_client(client_id, name)
            messagebox.showinfo("Success!", f"Client {client_id} was added.")
        self.on_entity_change()

    def remove_something(self):
        entity = self.entity_var.get()
        selection = self.book_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning!", "No item  selected!")
            return
        if entity == "Book":
            book_title = simpledialog.askstring("Remove book", "Enter book title")
            if not book_title: return
            self._book_service.remove_book(book_title)
            messagebox.showinfo("Success!", f"Book {book_title} was removed.")

        elif entity == "Client":
            client_id = simpledialog.askstring("Remove client", "Enter client id")
            if not client_id: return
            self._client_service.remove_client(client_id)
            messagebox.showinfo("Success!", f"Client {client_id} was removed.")
        self.on_entity_change()

    def update_something(self):
        entity = self.entity_var.get()
        selection = self.book_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning!", "No item selected!")
            return
        if entity == "Book":
            book_id = simpledialog.askstring("Update book", "Enter book id")
            if not book_id: return
            new_title = simpledialog.askstring("Update book", "Enter new book title")
            if not new_title: return
            new_author = simpledialog.askstring("Update book", "Enter new book author")
            if not new_author: return
            self._book_service.update_book(book_id, new_title, new_author)
            messagebox.showinfo("Success!", f"Book {book_id} was updated.")

        elif entity == "Client":
            client_id = simpledialog.askstring("Update client", "Enter client id")
            if not client_id: return
            new_name = simpledialog.askstring("Update client", "Enter new client name")
            if not new_name: return
            self._client_service.update_client(client_id, new_name)
            messagebox.showinfo("Success!", f"Client {client_id} updated.")
        self.on_entity_change()

    def perform_search(self):
        entity = self.search_entity_var.get()
        search_by = self.search_by_var.get()
        value = self.search_value_entry.get()
        if not value:
            messagebox.showwarning("Warning!", "Please enter a search term.")
            return
        results = []
        if entity == "Book":
            if search_by == "id":
                results = self._book_service.search_book_id(value)
            elif search_by == "title":
                results = self._book_service.search_book_title(value)
            elif search_by == "author":
                results = self._book_service.search_book_author(value)
        elif entity == "Client":
            if search_by == "id":
                results = self._client_service.search_client_id(value)
            elif search_by == "name":
                results = self._client_service.search_client_name(value)
        self.update_listbox(self.search_listbox, results)
        if not results:
            messagebox.showinfo("Search result", "No results found.")

    def rent_book(self):
        try:
            client_id = self.rent_client_id_entry.get().strip()
            book_title = self.rent_book_title_entry.get().strip()
            if not client_id or not book_title:
                messagebox.showwarning("Warning!", "Please enter a client and a book title.")
                return
            rental_id = self._rental_service.generate_rental_id()
            rented_date = str(date.today())
            returned_date = ""
            self._rental_service.rent_book(rental_id, client_id, book_title, rented_date, returned_date)
            messagebox.showinfo("Success!", f"Book {book_title} was rented to {client_id}.")
            self.on_entity_change()
            self.rent_client_id_entry.delete(0, tk.END)
            self.rent_book_title_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error!", f"Something went wrong! {e}")

    def return_book(self):
        try:
            book_title = self.return_book_title_entry.get().strip()
            if not book_title:
                messagebox.showwarning("Warning!", "Please enter a book title.")
                return
            self._rental_service.return_book(book_title)
            messagebox.showinfo("Success!", f"Book {book_title} was returned.")
            self.return_book_title_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error!", f"Something went wrong! {e}")

    def list_all_rentals(self):
        rentals = self._rental_service.list_rentals()
        self.update_listbox(self.rental_listbox, rentals)
        if not rentals:
            messagebox.showinfo("Info", "No rentals found.")

    def most_rented_books(self):
        try:
            most_rented =self._statistics_service.get_most_rented_books()
            display_list = []
            for i, r in enumerate(most_rented):
                if i < 5:
                    display_list.append(f"{i+1}. {r.name} -- Rentals: {r.value}")
            self.update_listbox(self.s1_listbox, display_list)
        except Exception as e:
            messagebox.showerror("Error!", f"Something went wrong! {e}")

    def most_active_clients(self):
        try:
            most_active =self._statistics_service.get_most_active_clients()
            display_list = []
            for i, r in enumerate(most_active):
                if i < 5:
                    display_list.append(f"{i+1}. {r.name} -- Days rented: {r.value}")
            self.update_listbox(self.s2_listbox, display_list)
        except Exception as e:
            messagebox.showerror("Error!", f"Something went wrong! {e}")

    def most_rented_authors(self):
        try:
            most_rented =self._statistics_service.get_most_rented_authors()
            display_list = []
            for i, r in enumerate(most_rented):
                if i < 5:
                    display_list.append(f"{i+1}. {r.name} -- Rentals: {r.value}")
            self.update_listbox(self.s3_listbox, display_list)
        except Exception as e:
            messagebox.showerror("Error!", f"Something went wrong! {e}")

    def undo_operation(self):
        try:
            self._undo_service.undo()
            messagebox.showinfo("Undo","Undo operation finished")
            self.on_entity_change()
            self.list_all_rentals()
            self.most_rented_books()
            self.most_active_clients()
            self.most_rented_authors()
        except Exception as e:
            messagebox.showerror("Error!", f"Something went wrong! {e}")

    def redo_operation(self):
        try:
            self._undo_service.redo()
            messagebox.showinfo("Redo","Redo operation finished")
            self.on_entity_change()
            self.list_all_rentals()
            self.most_rented_books()
            self.most_active_clients()
            self.most_rented_authors()
        except Exception as e:
            messagebox.showerror("Error!", f"Something went wrong! {e}")

if __name__ == "__main__":
    services = GUI._user_run_init()
    if services[0] is not None:
        root = tk.Tk()
        style = ttk.Style()
        style.theme_use('clam')
        app = GUI(root, *services)
        root.mainloop()
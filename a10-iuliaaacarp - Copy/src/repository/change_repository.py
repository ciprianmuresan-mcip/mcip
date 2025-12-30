import os

from src.repository.book_repository import *
from src.repository.client_repository import *
from src.repository.rental_repository import *

class SettingsManager:
    def __init__(self, file):
        self._file = os.path.abspath(file)
        self._settings = {}
        self.__load_setting()

    def __load_setting(self):
        try:
            with open(self._file, "r") as fin:
                for line in fin:
                    if "=" in line:
                        key, value = line.split("=", 1)
                        self._settings[key.strip()] = value.strip()
        except FileNotFoundError:
            raise FileNotFoundError("Settings file not found")

    def get(self, key: str, default=None):
        return self._settings.get(key, default)

class RepositoryChange:
    def __init__(self, setting_file):
        self.settings = SettingsManager(setting_file)

    def create_repo_book(self):
        repo = self.settings.get("repository","text").lower()
        if repo == "text":
            return BookTextFileRepository("books.txt")
        elif repo == "memory":
            return BookMemoryRepository()
        elif repo == "binary":
            return BookBinaryFileRepository("books.bin")
        else:
            raise ValueError("Repository not supported")

    def create_repo_client(self):
        repo = self.settings.get("repository","text").lower()
        if repo == "text":
            return ClientTextFileRepository("clients.txt")
        elif repo == "memory":
            return ClientMemoryRepository()
        elif repo == "binary":
            return ClientBinaryFileRepository("clients.bin")
        else:
            raise ValueError("Repository not supported")

    def create_repo_rental(self):
        repo = self.settings.get("repository","text").lower()
        if repo == "text":
            return RentalTextFileRepository("rentals.txt")
        elif repo == "memory":
            return RentalMemoryRepository()
        elif repo == "binary":
            return RentalBinaryFileRepository("rentals.bin")
        else:
            raise ValueError("Repository not supported")

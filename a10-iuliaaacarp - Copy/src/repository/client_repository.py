import pickle
from src.domain.client_domain import Client


class ClientError(Exception):
    pass


class DuplicateIDError(ClientError):
    pass


class ClientNotFoundError(ClientError):
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


class ClientMemoryRepository:
    def __init__(self):
        self._data = {}

    def get_client(self, client_id: str) -> Client:
        if client_id not in self._data:
            raise ClientNotFoundError(f"Client {client_id} not found")
        return self._data[client_id]

    def add_client(self, client: Client):
        if client.get_client_id in self._data:
            raise DuplicateIDError("Duplicate Client ID")
        self._data[client.get_client_id] = client

    def remove_client(self, client_id: str) -> Client:
        """
        Removes a client by name and returns the removed Client object.
        """
        if client_id not in self._data:
            raise ClientNotFoundError(f"Client with id '{client_id}' not found.")
        deleted_client = None

        for client in self._data.values():
            if client_id == client.get_client_id:
                deleted_client = client
                break

        del self._data[client_id]
        return deleted_client


    def update_client(self, client_id: str, client_name: str):
        if client_id not in self._data:
            raise ClientNotFoundError(f"Client ID '{client_id}' not found.")
        self._data[client_id] = Client(client_id, client_name)

    def display_all_clients(self) -> list[Client]:
        return list(self._data.values())

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return RepositoryIterator(list(self._data.values()))


class ClientBinaryFileRepository(ClientMemoryRepository):
    def __init__(self, filename: str = "clients.bin"):
        super().__init__()
        self._filename = filename
        self.__load_file()

    def add_client(self, client: Client):
        super().add_client(client)
        self.__save_file()

    def remove_client(self, client_id: str) -> Client:
        deleted_client = super().remove_client(client_id)
        self.__save_file()
        return deleted_client

    def update_client(self, client_id: str, client_name: str):
        super().update_client(client_id, client_name)
        self.__save_file()

    def __save_file(self):
        try:
            with open(self._filename, "wb") as fout:
                pickle.dump(self._data, fout)
        except Exception:
            pass

    def __load_file(self):
        try:
            with open(self._filename, "rb") as fin:
                self._data = pickle.load(fin)
        except FileNotFoundError:
            self._data = {}


class ClientTextFileRepository(ClientMemoryRepository):
    def __init__(self, filename: str = "clients.txt"):
        super().__init__()
        self._filename = filename
        self.__load_file()

    def add_client(self, client: Client):
        super().add_client(client)
        self.__save_file()

    def remove_client(self, client_id: str) -> Client:
        deleted_client = super().remove_client(client_id)
        self.__save_file()
        return deleted_client

    def update_client(self, client_id: str, client_name: str):
        super().update_client(client_id, client_name)
        self.__save_file()

    def __load_file(self):
        try:
            with open(self._filename, "r") as fin:
                self._data = {}
                for line in fin:
                    part = line.strip().split(", ")
                    if len(part) != 2:
                        continue
                    client_id, client_name = part
                    self._data[client_id] = Client(client_id, client_name)
        except FileNotFoundError:
            self._data = {}

    def __save_file(self):
        with open(self._filename, "w") as fout:
            for client in self._data.values():
                fout.write(f"{client.get_client_id}, {client.get_client_name}\n")
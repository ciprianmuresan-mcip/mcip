import random
from src.domain.client_domain import Client
from src.services.undo_service import UndoService, Operation, FunctionCall


class ClientService:
    def __init__(self, client_repo, undo_service: UndoService):
        self._client_repo = client_repo
        self._undo_service = undo_service

    def get_client(self, client_id):
        return self._client_repo.get_client(client_id)

    @staticmethod
    def generate_client_id():
        return str(random.randint(10000, 99999))

    def add_client(self, client_id, client_name):
        client = Client(client_id, client_name)
        self._client_repo.add_client(client)

        undo_function = FunctionCall(self._client_repo.remove_client, client_name)
        redo_function = FunctionCall(self._client_repo.add_client, client)

        self._undo_service.record(Operation(undo_function, redo_function))

    def remove_client(self, client_id):
        deleted_client = self._client_repo.remove_client(client_id)

        undo_function = FunctionCall(self._client_repo.add_client, deleted_client)
        redo_function = FunctionCall(self._client_repo.remove_client, client_id)

        self._undo_service.record(Operation(undo_function, redo_function))

    def update_client(self, client_id, client_name):
        original_client = self._client_repo.get_client(client_id)
        original_name = original_client.get_client_name

        self._client_repo.update_client(client_id, client_name)

        undo_function = FunctionCall(self._client_repo.update_client, client_id, original_name)
        redo_function = FunctionCall(self._client_repo.update_client, client_id, client_name)

        self._undo_service.record(Operation(undo_function, redo_function))

    def display_all_clients(self):
        return list(self._client_repo)

    def search_client_id(self, client_id):
        search = []
        client_id_str = str(client_id).lower()
        for client in self._client_repo:
            if client_id_str in str(client.get_client_id).lower():
                search.append(client)
        return search

    def search_client_name(self, client_name):
        search = []
        client_name_str = str(client_name).lower()
        for client in self._client_repo:
            if client_name_str in client.get_client_name.lower():
                search.append(client)
        return search

    def search_client_name_id(self, client_name):
        client_name_str = str(client_name).lower()
        for client in self._client_repo:
            if client_name_str == client.get_client_name.lower():
                return client.get_client_id
        return None

    def get_client_name_by_id(self, client_id):
        client = self._client_repo.get_client(client_id)
        return client.get_client_name

    @property
    def client_repo(self):
        return self._client_repo
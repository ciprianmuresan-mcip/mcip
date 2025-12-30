class Client:
    """
    Represents a client in the library
    """
    def __init__(self, client_id: str, client_name: str):
        """
        Initialize the client
        :param client_id: the unique id of the client
        :param client_name: the name of the client
        """
        self._client_id = client_id
        self._client_name = client_name

    @property
    def get_client_id(self):
        """
        :return: the unique id of the client
        """
        return self._client_id

    @property
    def get_client_name(self):
        """
        :return: the name of the client
        """
        return self._client_name

    def __str__(self):
        """
        :return: a string representation of the client
        """
        return f"ID: {self.get_client_id}| {self.get_client_name}"

    def __repr__(self):
        return self.__str__()
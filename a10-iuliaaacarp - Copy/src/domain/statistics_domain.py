class RentalStats:
    def __init__(self, name: str, value: int, second_value: str = None):
        self.name = name
        self.value = value
        self.second_value = second_value

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self):
        if self.second_value:
            return f"{self.name}-{self.second_value} days | Book: {self.second_value}"
        return f"{self.name}-{self.value}"
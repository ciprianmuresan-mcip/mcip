import string
from texttable import Texttable

class BattleshipException(Exception):
    pass

class Board:
    def __init__(self):
        self._rows = 6
        self._columns = 6
        self._data = [[0 for _ in range(6)] for _ in range(6)]

    def place_ship(self, r, c, ori):
        coords = []
        for i in range(3):
            curr_r, curr_c = (r, c + i) if ori == 'H' else (r + i, c)

            if not (0 <= curr_r < 6 and 0 <= curr_c < 6):
                raise BattleshipException("Ship out of bounds!")
            if self._data[curr_r][curr_c] == 1:
                raise BattleshipException("Ships cannot overlap!")
            coords.append((curr_r, curr_c))

        for row, col in coords:
            self._data[row][col] = 1

    def fire(self, r, c):
        if self._data[r][c] in (2, 3):
            raise BattleshipException("Square already targeted!")

        if self._data[r][c] == 1:
            self._data[r][c] = 3
            return True
        else:
            self._data[r][c] = 2
            return False

    def is_defeated(self):
        return not any(1 in row for row in self._data)

    @staticmethod
    def _get_header():
        return [' '] + list(string.ascii_uppercase[:6])

class PlayerBoard(Board):
    def __str__(self):
        t = Texttable()
        t.header(self._get_header())
        mapping = {0: ' ', 1: 'S', 2: '.', 3: 'X'}
        for i, row in enumerate(self._data):
            t.add_row([str(i + 1)] + [mapping[cell] for cell in row])
        return t.draw()

class TargetingBoard(Board):
    def __str__(self):
        t = Texttable()
        t.header(self._get_header())
        mapping = {0: ' ', 1: ' ', 2: '.', 3: 'X'}
        for i, row in enumerate(self._data):
            t.add_row([str(i + 1)] + [mapping[cell] for cell in row])
        return t.draw()
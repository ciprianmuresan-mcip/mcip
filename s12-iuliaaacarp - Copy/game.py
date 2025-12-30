from random import shuffle, choice
from board import PlayerBoard, TargetingBoard, BattleshipException

class Game:
    def __init__(self):
        self.player_board = PlayerBoard()
        self.computer_board = TargetingBoard()
        self.computer_shots = [(r, c) for r in range(6) for c in range(6)]
        shuffle(self.computer_shots)

    def setup_computer_ships(self):
        ships_placed = 0
        while ships_placed < 2:
            r = choice(range(6))
            c = choice(range(6))
            ori = choice(['H', 'V'])
            try:
                self.computer_board.place_ship(r, c, ori)
                ships_placed += 1
            except BattleshipException:
                continue

    def computer_turn(self):
        if not self.computer_shots:
            return None, False
        r, c = self.computer_shots.pop()
        hit = self.player_board.fire(r, c)
        return (r, c), hit
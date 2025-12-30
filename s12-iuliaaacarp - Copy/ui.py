import string
from game import Game
from board import BattleshipException

class UI:
    def __init__(self):
        self._game = Game()

    @staticmethod
    def _parse_coords(cmd):
        try:
            if len(cmd) < 2: raise ValueError
            col = string.ascii_uppercase.index(cmd[0].upper())
            row = int(cmd[1:]) - 1
            return row, col
        except:
            raise BattleshipException("Invalid format! Use ColumnLetterRowNumber (e.g., A1)")

    def phase1(self):
        print("--- Phase 1: Ship Placement ---")
        ships_placed = 0
        while ships_placed < 2:
            print(self._game.player_board)
            try:
                user_input = input(f"Place ship {ships_placed + 1}/2 (Coord Ori): ").split()
                if len(user_input) < 2:
                    print("Error: Provide coordinate AND orientation")
                    continue

                r, c = self._parse_coords(user_input[0])
                ori = user_input[1].upper()

                self._game.player_board.place_ship(r, c, ori)
                ships_placed += 1
                print("Ship placed successfully!")
            except BattleshipException as e:
                print(f"Error: {e}")

        print("Final Player Setup:")
        print(self._game.player_board)
        self._game.setup_computer_ships()

    def phase2(self):
        print("--- Phase 2: Battle! ---")
        while True:
            print("COMPUTER BOARD (Targeting)")
            print(self._game.computer_board)
            print("YOUR BOARD")
            print(self._game.player_board)

            try:
                cmd = input("Fire at: ")
                r, c = self._parse_coords(cmd)
                hit = self._game.computer_board.fire(r, c)
                print(f"YOUR SHOT: {'HIT!' if hit else 'MISS!'}")
            except Exception as e:
                print(f"Error: {e}")
                continue

            if self._game.computer_board.is_defeated():
                print("VICTORY! All enemy ships sunk!")
                break

            coords, hit = self._game.computer_turn()
            col_char = string.ascii_uppercase[coords[1]]
            print(f"COMPUTER SHOT at {col_char}{coords[0] + 1}: {'HIT!' if hit else 'MISS!'}")

            if self._game.player_board.is_defeated():
                print("DEFEAT! All your ships were sunk!")
                break

    def run(self):
        self.phase1()
        self.phase2()

if __name__ == '__main__':
    ui = UI()
    ui.run()
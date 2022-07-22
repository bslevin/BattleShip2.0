


# Holds the state of a player and their game board
class GameBoard:

    def __init__(self, name: str):
        # Only store first 16 characters of input name to ensure the printed nameplate looks nice
        self.name = name[:16]

    # Players have both a board and public-facing board to facilitate information hiding when displaying the board
        self.board = []
        self.public_board = []

        self.ships = 0

        self.clear()





# Holds the state of a player and their game board
class GameBoard:

    def __init__(self, name: str):
        # Only store first 16 characters of input name to ensure 
        # the printed nameplate looks nice
        self.name = name[:16]

        # Players have both a board and public-facing board to 
        # facilitate information hiding when displaying the board
        self.board = []
        self.public_board = []

        self.ships = 0

        self.clear()

    # Called to reset the game board, placing empty spaces at all coordinates
    def clear(self):
        placed_ships = 0
        while placed_ships < NUMBER_OF_SHIPS:
            x = randint(0, BOARD_SIZE - 1)
            y = randint(0, BOARD_SIZE - 1)


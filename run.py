from colorama import init, Fore, Back, Style
from random import randint
from re import sub

# Lookup table used to convert from column number to column letter
COL_LOOKUP = "ABCDEFGH"

# Filter ANSI escape sequences out of any text sent to stdout or stderr on Windows and replace with equiv.
# Set autoreset to True so that styles are automatically reset after every printed message
init(autoreset=True)

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

           # Skip to the next iteration if a ship has already been placed here
            if self.board[x][y] == BOARD_SHIP:
                continue

            self.board[x][y] = BOARD_SHIP
            placed_ships += 1

        self.ships = placed_ships
 
    # Called to display the game board within the terminal
    def display(self, public: bool = False):
        board_name = self.name + "'s Board"
        print(NAMEPLATE_STYLE +
              f"================================\n"
              f"{board_name:^32}\n"
              f"================================")

    # Print the header row of the game board
        print(BOARD_SEP.join(" ABCDEFGH"))

        for i in range(BOARD_SIZE):
            # Print row number and its corresponding row of the game board
            if public:
                print(i, *self.public_board[i], sep=BOARD_SEP)
            else:
                print(i, *self.board[i], sep=BOARD_SEP)

    # Called to check if a given coordinate has already been guessed on this game board
    def check_coord_guessed(self, col: int, row: int):
        return self.public_board[row][col] in [BOARD_MISS, BOARD_HIT]

    # Called to make a shot on a given coordinate
    def shoot_coordinates(self, col: int, row: int):
        # Ship hit
        if self.board[row][col] == BOARD_SHIP:
            self.board[row][col] = BOARD_HIT
            self.public_board[row][col] = BOARD_HIT
            self.ships -= 1
            return True

        # Ship missed
        self.board[row][col] = BOARD_MISS
        self.public_board[row][col] = BOARD_MISS
        return False

def main():
    print(TITLE_STYLE + TITLE_TXT)
    print(LOGO_STYLE + LOGO_TEXT)

    prompt_for_instructions()

    # Initialize a game board for the player with their given name
    player_board = GameBoard(input(PROMPT_STYLE + NAME_PROMPT))

from colorama import init, Fore, Back, Style
from random import randint
from re import sub

# Lookup table used to convert from column number to column letter
COL_LOOKUP = "ABCDEFGH"

# Filter ANSI escape sequences out of any text sent to stdout or stderr on Windows and replace with equiv. WIN32 calls
# Set autoreset to True so that styles are automatically reset after every printed message
init(autoreset=True)

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

    # Called to reset the game board, placing empty spaces at all coordinates
    def clear(self):
        self.board = [[BOARD_WAVE for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.public_board = [[BOARD_WAVE for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    # Called to place ships on the board at random locations
    def place_ships(self):
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
    # Initialize a game board for our AI
    comp_board = GameBoard("HAL")

    while True:
        player_board.place_ships()
        comp_board.place_ships()

        game_loop(player_board, comp_board)

        # Break from the main loop if the player doesn't wish to play another game
        if not prompt_for_new_game():
            break

        player_board.clear()
        comp_board.clear()

    print(Style.RESET_ALL + "\nGoodbye!")

# Main execution loop of the game. Called once the game boards are setup and ready
def game_loop(player: GameBoard, comp: GameBoard):
    while True:
        # Display Player's game board and the AI's public-facing game board
        player.display()
        comp.display(public=True)

        # Shoot at Player's desired coordinates on the AI's game board
        if comp.shoot_coordinates(*prompt_for_coordinates(comp)):
            print(SHOT_STYLE + f"\nYour shot was a hit! {comp.name} has {comp.ships} ship(s) remaining.")

            # End the game if player has destroyed the AI's last ship
            if not comp.ships:
                return end_game(player, comp)

        else:
            print(SHOT_STYLE + f"\nYour shot was a miss!")

        col, row = chose_random_coordinates(player)

        # Shoot at randomly chosen coordinates on the Player's game board
        if player.shoot_coordinates(col, row):
            print(SHOT_STYLE +
                  f"\n{comp.name} hit your ship at {COL_LOOKUP[col]}{row}. You have {player.ships} ship(s) remaining.")

            # End the game if the AI has destroyed the Player's last ship
            if not player.ships:
                return end_game(player, comp)

        else:
            print(SHOT_STYLE + f"\n{comp.name} shot and missed at {COL_LOOKUP[col]}{row}.")

# Called once one of the player's has zero ships remaining
def end_game(player: GameBoard, comp: GameBoard):
    # Display both player's full game board
    player.display()
    comp.display()

    # AI Won
    if not player.ships:
        print(ERROR_STYLE + DEFEAT_TEXT)
    # Player Won
    else:
        print(PROMPT_STYLE + VICTORY_TEXT)

# Called at the beginning of the game to check if the player needs instructions
def prompt_for_instructions():
    while True:
        # Ensure user inputs only a valid integers
        try:
            user_input = int(input(PROMPT_STYLE + INSTRUCTIONS_PROMPT))
        except ValueError:
            print(ERROR_STYLE + ERROR_MESSAGE)
            continue

        if user_input == 1:
            print(MESSAGE_STYLE + INSTRUCTIONS_TXT)
        elif user_input == 2:
            print(MESSAGE_STYLE + GAME_START_TXT)
            return
        else:
            print(ERROR_STYLE + ERROR_MESSAGE)

# Called to chose random coordinates for the AI
def chose_random_coordinates(player: GameBoard):
    x = randint(0, BOARD_SIZE - 1)
    y = randint(0, BOARD_SIZE - 1)

    # Ensure the returned coordinate hasn't already been guessed
    while player.check_coord_guessed(x, y):
        x = randint(0, BOARD_SIZE - 1)
        y = randint(0, BOARD_SIZE - 1)
    
    return x, y
    
# Called to get coordinates from the Player
def prompt_for_coordinates(comp: GameBoard):
    while True:
        # Remove any non-word characters from the Player's input
        user_input = sub(r"\W", '', input(PROMPT_STYLE + COORDINATE_PROMPT))
        
        # Ensure the given coordinates are valid
        if len(user_input) != 2 or not user_input[0].isalpha() or not user_input[1].isnumeric():
            print(ERROR_STYLE + COORDINATE_ERR_MSG)
            continue

        # Convert column letter into column number
        col = ord(user_input[0].upper()) - 65
        # Convert row number into an integer
        row = int(user_input[1])
   
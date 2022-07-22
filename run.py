


# Holds the state of a player and their game board
class GameBoard:

    def __init__(self, name: str):
        # Only store first 16 characters of input name to ensure the printed nameplate looks nice
        self.name = name[:16]

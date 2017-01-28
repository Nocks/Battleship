from board import Board
# The available ships for the battle

class Player:
    SHIP_INFO = [
        ("Aircraft Carrier", 5),
        ("Battleship", 4),
        ("Submarine", 3),
        ("Cruiser", 3),
        ("Patrol Boat", 2)
    ]

    def get_player_name(self):
        while True:
            self.name = input("Name: ").strip()
            if len(self.name) == 0:
                print("Kindly enter a name.")
                continue
            else:
                self.name = self.name.title()
                return self.name
                break

    def prepare_ships(self):
        self.ships = []
        for ship in self.SHIP_INFO:
            self.ships.append(ship)
        return self.ships

    def __init__(self):
        self.name = self.get_player_name()
        self.opponent = None
        self.board = Board()
        self.ships = self.prepare_ships()
        self.ship_details = {}
        self.shot_ships = {}
        self.occupied_spots = []
        self.good_guesses = []
        self.bad_guesses = []

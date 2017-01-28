from ship import Ship
from gameerrors import InvalidFormatError
from gameerrors import PositionOccupiedError
from gameerrors import ShipOverlapError


class Board:
    VERTICAL_SHIP = '|'
    HORIZONTAL_SHIP = '-'
    BOARD_SIZE = 10
    EMPTY = 'O'
    ACCEPTED_COL = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    ACCEPTED_ROW = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def __init__(self):
        self.self_board = [[self.EMPTY for n in range(10)] for n in range(10)]
        self.guess_board = [[self.EMPTY for n in range(10)] for n in range(10)]

    def print_board_heading(self):
        print("   " + " ".join([chr(c) for c in range(ord('A'), ord('A') + self.BOARD_SIZE)]))

    def print_board(self, board):
        self.print_board_heading()

        row_num = 1
        for row in board:
            print(str(row_num).rjust(2) + " " + (" ".join(row)))
            row_num += 1

    def update_board(self, ship, cordinate, orientation):
        row = cordinate[0]
        col = cordinate[1]
        if orientation == 'v':
            for x in range(ship[1]):
                self.self_board[row][col] = self.VERTICAL_SHIP
                row += 1
        elif orientation == 'h':
            for x in range(ship[1]):
                self.self_board[row][col] = self.HORIZONTAL_SHIP
                col += 1

    def validate_placement(self, cordinate):
        """Checks to see if the user input is in the correct format.
        e.g: a2, b4, d7, etc. Otherwise, returns False
        """
        cordinate = cordinate.strip()
        cordinate = cordinate.lower()
        if cordinate == "" or len(cordinate) < 2 or len(cordinate) > 3:
            raise InvalidFormatError
        elif cordinate[0].isalpha() == False:
            raise InvalidFormatError
        elif cordinate[1:].isnumeric() == False:
            raise InvalidFormatError
        elif cordinate[0] not in self.ACCEPTED_COL:
            raise InvalidFormatError
        elif int(cordinate[1:]) not in  self.ACCEPTED_ROW:
            raise InvalidFormatError
        else:
            return True

    def ask_for_placement(self, player, ship, length):
        """Asks the player where they want to place their current ship"""
        placement_point = input(
            "\n{}, where do you want to place your {} of length {}? "
              .format(player, ship, length))
        return placement_point

    def ask_for_orientation(self, ship):
        """Asks the player how they want to place their ship"""
        while True:
            orientation = input("How do you want to place the {}? [V]ertically or [H]orizontally? "
                                .format(ship)).strip()
            orientation = orientation.lower()
            if orientation not in Ship.orientation:
                print("\n***{} is an invalid input. Enter either 'V' or 'H'.***"
                      .format(orientation))
                continue
            else:
                return orientation

    def convert_ship_spot(self, spot):
        """This method converts the ship's spot (player's input) into
        a tuple of coordinates that can be used with the board
        E.g: b4 becomes (3,1), and so on"""
        spot = spot.lower()
        y = spot[0]
        x = spot[1:]
        x = int(x)
        x -= 1
        # The column of the board
        board_col = 'abcdefghij'
        y = board_col.index(y)
        return x,y

    def generate_occupied_spots(self, player, ship, cordinate, orientation):
        """This method loops through the length of the given ship from where
        the ship was placed on the board. In the end, it generates
        all the spots the ship covers on the board."""
        row = cordinate[0]
        col = cordinate[1]
        occupied_spots = []
        if orientation == 'v':
            for x in range(ship[1]):
                occupied_spots.append((row,col))
                row += 1
            # Assign the ship its corresponding occupied spots
            # E.g ship_details['Submarine'] = [(5,0), (6,0), (7,0), (8,0)]
            player.ship_details[ship[0]] = occupied_spots
            return occupied_spots

        elif orientation == 'h':
            for x in range(ship[1]):
                occupied_spots.append((row,col))
                col += 1
            # Assign the ship its corresponding occupied spots
            # E.g ship_details['Submarine'] = [(5,0), (6,0), (7,0), (8,0)]
            player.ship_details[ship[0]] = occupied_spots
            return occupied_spots

    def update_occupied_spots(self, player, generate_occupied_spots):
        player.occupied_spots.append(generate_occupied_spots)

    def check_board_range(self, ship_length, spot, cordinate, orientation):
        if ((self.BOARD_SIZE - (cordinate[0] + 0)) >= int(ship_length)
            and orientation == 'v'):
            return True
        elif ((self.BOARD_SIZE - (cordinate[1])) >= int(ship_length)
            and orientation == 'h'):
            return True
        else:
            raise PositionOccupiedError

    def check_for_overlaps(self, player, generated_occupied_spots):
        """This uses the passed cordinate and checks if it already
        exists in the occupied_spots"""
        for occupied_spot in generated_occupied_spots:
            if not occupied_spot in player.occupied_spots:
                player.board.update_occupied_spots(player, occupied_spot)
            else:
                raise ShipOverlapError

import os
import random

from board import Board
from player import Player
from ship import Ship
from gameerrors import InvalidFormatError
from gameerrors import PositionOccupiedError
from gameerrors import ShipOverlapError


class Battleship():
    MISS = '.'
    HIT = '*'
    SUNK = '#'
    DEFEAT = False
    error_input = ("\n***{} is an invalid input! a - j and 1 - 10 are "
                   "only allowed. e.g b2***")
    error_unfit = ("\n***{0} is an invalid location. {1} cannot fit on board "
                   "at {0}.***")
    error_overlap = "\n***Sorry! {} overlaps with another ship at {}.***"

    def __init__(self):
        self.players = None

    def clear_screen(self):
        try:
          os.system('cls')
        except:
          os.system('clear')

    def register_players(self):
        """Setup players for the battle"""
        self.clear_screen()
        print("Player 1")
        self.player1 = Player()
        self.clear_screen()
        while True:
            print("Player 2")
            self.player2 = Player()
            # Check to see if name of player2 in same as that of player 1
            if self.player1.name == self.player2.name:
                self.clear_screen()
                print("\n***Name of Player 2 must be different from that of Player 1.***")
                continue
            else:
                break

        self.players = [self.player1, self.player2]
        self.players[0].opponent = self.player2
        self.players[1].opponent = self.player1

    def confirm_registration(self):
        """Inform players of successful registration"""
        self.clear_screen()
        input("Great! {} is player 1 and {} is player 2.\n\n"
              .format(self.players[0].name, self.players[1].name) +
              "Press enter to continue... ")

    def place_ship(self):
        """Prompt the player to place ship on board one at a time."""
        for turn in range(2):
            if ((self.players[turn] == self.player1)
                and (self.players[turn].ships != None)):
                self.clear_screen()
                self.players[turn].board.print_board(self.player1.board.self_board)
                self.process_placement(self.players[turn])
                input("\nGreat, {}! Your ships are set for the battle. Press enter to continue... ".format(self.players[turn].name))

            elif ((self.players[turn] == self.player2)
                  and (self.players[turn].ships != None)):
                self.clear_screen()
                self.players[turn].board.print_board(self.player2.board.self_board)
                self.process_placement(self.players[turn])
                input("\nGreat, {}! Your ships are set for the battle. Press enter to continue... ".format(self.players[turn].name))
                self.clear_screen()
                input("The battle starts now! {} is the first to shoot.\nPress enter to start... ".format(self.players[0].name))

    def process_placement(self, player):
        for current_ship in player.ships:
            while True:
                # Placement_point is the input from the player (a2, d3, etc)
                placement_point = player.board.ask_for_placement(
                    player.name,
                    current_ship[0],
                    current_ship[1]
                )
                try:
                    player.board.validate_placement(placement_point)
                    orientation = player.board.ask_for_orientation(current_ship[0])
                    cordinate = player.board.convert_ship_spot(placement_point)
                    player.board.check_board_range(
                        current_ship[1],
                        placement_point,
                        cordinate,
                        orientation)
                    generated_occupied_spots = player.board.generate_occupied_spots(
                        player,
                        current_ship,
                        cordinate,
                        orientation)
                    player.board.check_for_overlaps(player, generated_occupied_spots)
                    player.board.update_board(current_ship, cordinate, orientation)
                except InvalidFormatError:
                    print(self.error_input.format(placement_point.upper()))
                except PositionOccupiedError:
                    print(self.error_unfit.format(placement_point.upper(), current_ship[0]))
                except ShipOverlapError:
                    print(self.error_overlap.format(current_ship[0], placement_point.upper()))
                else:
                    self.clear_screen()
                    player.board.print_board(player.board.self_board)
                    break

    def shoot_ships(self, players):
        """This method makes players shoot ships in turns."""
        while self.DEFEAT != True:
            for player in players:
                shoot_result = self.ask_for_spot_to_shoot_at(player)
                self.display_guessed_results(player, shoot_result)
                if self.check_defeat(player):
                    self.DEFEAT = True
                    print("\nYour board:\n".format(player.name.title()))
                    player.board.print_board(player.board.self_board)

                    print("\n{}'s board:\n".format(player.opponent.name.title()))
                    player.opponent.board.print_board(
                        player.opponent.board.self_board)
                    break
                else:
                    self.clear_screen()
                    input("{}, it's your turn. Press enter to guess... "
                          .format(player.opponent.name.title()))

    def ask_for_spot_to_shoot_at(self, player):
        """Prompts the player where they want to shoot opponent’s ship"""
        self.clear_screen()
        while True:
            print("Below are your guesses on {}'s board so far:\n"
                  .format(player.opponent.name.title()))
            player.board.print_board(player.board.guess_board)
            print("\nBelow are {}'s guesses on your board so far:\n"
                  .format(player.opponent.name.title()))
            player.opponent.board.print_board(player.board.self_board)
            spot = input("\n{} where do you want to shoot at? "
                         .format(player.name.title()))
            try:
                player.board.validate_placement(spot)
                guessed_spot = player.board.convert_ship_spot(spot)

                if (guessed_spot in player.good_guesses
                    or guessed_spot in player.bad_guesses):
                    input("\n***{}, you've already guessed {}! Press enter and try again.***"
                          .format(player.name.title(), spot.upper()
                    ))
                    self.clear_screen()
                    continue

                    # Check to see if the guessed spot is in the opponent's
                    # occupied_spots. If so, it's a good guess.
                    # Add the guessed_spot to the player's list of good_guesses.
                elif (guessed_spot in player.opponent.occupied_spots):
                    self.update_board_at_battle(
                        player,
                        guessed_spot,
                        player.opponent.board.self_board,
                        hit=True)
                    self.update_board_at_battle(
                        player,
                        guessed_spot,
                        player.board.guess_board,
                        hit=True)
                    self.downgrade_ship_life(player, guessed_spot)
                    player.good_guesses.append(guessed_spot)
                    return "hit"
                elif (guessed_spot not in player.opponent.occupied_spots):
                    self.update_board_at_battle(
                        player,
                        guessed_spot,
                        player.opponent.board.self_board,
                        hit=False)
                    self.update_board_at_battle(
                        player,
                        guessed_spot,
                        player.board.guess_board,
                        hit=False)
                    player.bad_guesses.append(guessed_spot)
                    return "miss"

            except InvalidFormatError:
                self.clear_screen()
                print(self.error_input.format(spot.upper()))
            else:
                break

    def downgrade_ship_life(self, player, spot):
        """This method is called when a ship is hit at 'spot'.
        It uses 'spot' to find corresponding ship in opponent's
        ship_details dictionary. When found, deletes the 'spot' from the value
        (list of tuples) of the ships. However, before it deletes the 'spot',
        it updates the opponent's shot_ships dict with the spot."""
        for ship, spots in player.opponent.ship_details.items():
            tmp_ship_details = []
            if spot in spots:
                # This part updates the opponent's shot_ships dict with the spot.
                if ship not in player.opponent.shot_ships.keys():
                    player.opponent.shot_ships[ship] = []
                    for key, value in player.opponent.shot_ships.items():
                        if key == ship:
                            value.append(spot)
                elif ship in player.opponent.shot_ships.keys():
                    for key, value in player.opponent.shot_ships.items():
                        if key == ship:
                            value.append(spot)
                tmp_ship_details = spots
                tmp_ship_details.remove(spot)
                player.opponent.ship_details[ship] = tmp_ship_details

    def display_guessed_results(self, player, result):
        if result == "hit":
            input("Good job, {}! You just hit one of {}'s ships. Press enter to continue... "
                  .format(player.name.title(), player.opponent.name.title()))
            self.check_sunken(player)

        elif result == "miss":
            input("Oh no, {}! That was a miss! Press enter to continue... "
                  .format(player.name.title()))

    def update_board_at_battle(self, player, spot, passed_board, hit=None):
        row = spot[0]
        col = spot[1]
        if hit == True and passed_board[row][col] != self.SUNK:
            passed_board[row][col] = self.HIT
            player.board.guess_board[row][col] = self.HIT
        if hit == False:
            passed_board[row][col] = self.MISS
            player.board.guess_board[row][col] = self.MISS

    def check_sunken(self, player):
        if player.opponent.ship_details:
            for ship_name, ship_value in player.opponent.ship_details.items():
                if len(ship_value) == 0:
                    input(("{}, you've just sunk {}'s {}. That was smart! Press enter to continue... ")
                          .format(player.name.title(),
                                  player.opponent.name.title(),
                                  ship_name))
                    self.update_board_sunken(player, ship_name)
                    player.opponent.ship_details.pop(ship_name)
                    break

    def update_board_sunken(self, player, ship_name):
        for ship, coordinates in player.opponent.shot_ships.items():
            if ship == ship_name:
                for spot in coordinates:
                    row = spot[0]
                    col = spot[1]
                    player.opponent.board.self_board[row][col] = self.SUNK
                    player.board.guess_board[row][col] = self.SUNK

    def check_defeat(self, player):
        """This method checks to see if opponent no longer has ships"""
        if not player.opponent.ship_details:
            self.clear_screen()
            input("{}, you've just defeated {}! Congratulation! Press enter to continue... "
                  .format(player.name.title(),
                          player.opponent.name.title()))
            return True

    def battle(self):
        self.clear_screen()
        input("Welcome to the Battleship Game!\nPlease press enter to register players... ")

        self.register_players()
        self.confirm_registration()
        self.place_ship()
        self.shoot_ships(self.players)

if __name__ == '__main__':
    game = Battleship()
    game.battle()

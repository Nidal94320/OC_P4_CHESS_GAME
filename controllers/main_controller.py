"""Main controller"""

from typing import List
from time import sleep
import sys

from models.players import Player
from models.tournaments import Tournament
from controllers.src.home_controller import HomeController
from controllers.src.players_controller import PlayersController
from controllers.src.rapport_controller import RapportController
from controllers.src.tournament_controller import TournamentController


class Controller:
    def __init__(self):
        # self.players: List[Player] = []

        self.home_controller = HomeController()
        self.players_controller = PlayersController()
        self.rapport_controller = RapportController()
        self.tournament_controller = TournamentController()

    def run(self):
        # initalize data for demo
        # home menu
        choice = self.home_controller.home_menu()

        if choice == "1":
            # players menu
            if self.players_controller.players_menu() == "exit":
                self.run()

        if choice == "2":
            # tournament menu
            if self.tournament_controller.tournament_menu() == "exit":
                self.run()

        if choice == "3":
            # rapport menu
            if self.rapport_controller.rapport_menu() == "exit":
                self.run()

        elif choice == "4":
            # exit game
            sys.exit()

        else:
            # return to Home menu if invalid choice
            choice = self.home_controller.home_menu()

        # est ce ici qu'il faut fermer le fichier JSON?
        Player.db().close()
        Tournament.db().close()

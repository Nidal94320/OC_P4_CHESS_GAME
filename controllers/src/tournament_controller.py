"""Tournament Menu controller"""


from views.view_tournament import ViewTournament
from models.players import Player
from models.tournaments import Tournament


class TournamentController:
    """Tournament Menu controller"""

    def __init__(self):
        self.tournament_view = ViewTournament()

    def tournament_menu(self):
        """tournament menu"""

        choice = self.tournament_view.tournament_menu()

        if choice == "1":
            """create"""

            self.tournament_menu()

        elif choice == "2":
            """play"""

            self.tournament_menu()

        elif choice == "3":
            """edit"""

            self.tournament_menu()

        elif choice == "4":
            """delete"""

            self.tournament_menu()

        elif choice == "5":
            """Back to Home Menu"""

            return "exit"

        else:
            """invalid choice"""
            self.tournament_view.invalid_choice()
            self.tournament_menu()

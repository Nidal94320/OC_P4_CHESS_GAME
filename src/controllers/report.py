"""class ReportController"""

from .common import clean_upper


from src.views.report import ReportView
from src.models.player import Players
from src.models.tournament import Tournaments


class ReportController:
    def __init__(self, view=ReportView()):
        self.view = view

    def run(self):
        """report menu"""

        choice = self.view.menu()

        if choice == "1":
            """list all players in the system"""

            Players.report()
            self.view.list_players(Players.read(), "registered", "system")
            self.run()

        elif choice == "2":
            """list all tournaments in the system"""

            tournaments_list = Tournaments.report()
            self.view.list_tournaments(tournaments_list, "created")
            self.run()

        elif choice == "3":
            """select a tournament"""

            choice_3 = clean_upper(self.view.tournament_name())
            if choice_3 in Tournaments.read_names():
                tournament_list = Tournaments.report(choice_3)
                self.view.list_tournaments(tournament_list, "selected")
            else:
                self.view.tournament_name_reponse()
            self.run()

        elif choice == "4":
            """list all players of one tournament"""

            choice_4 = clean_upper(self.view.tournament_name())
            if choice_4 in Tournaments.read_names():
                tournament4 = Tournaments.load(choice_4)
                tournament4_players = tournament4.players_name_report()
                self.view.list_players(tournament4_players, "registered", "tournament")
            else:
                self.view.tournament_name_reponse()
            self.run()

        elif choice == "5":
            """list all matchs and rounds of one tournament"""

            choice_5 = clean_upper(self.view.tournament_name())
            if choice_5 in Tournaments.read_names():
                tournament5 = Tournaments.load(choice_5)
                rounds_list = tournament5.rounds_report()
                self.view.list_rounds(rounds_list)
            else:
                self.view.tournament_name_reponse()
            self.run()

        elif choice == "6":
            """Back to Home Menu"""

            return "exit"

        else:
            """invalid choice"""

            self.run()

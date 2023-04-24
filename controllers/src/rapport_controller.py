"""Rapport Menu controller"""


from views.view_rapport import ViewRapport
from models.players import Player
from models.tournaments import Tournament


class RapportController:
    """Rapport Menu controller"""

    def __init__(self):
        self.rapport_view = ViewRapport()

    def rapport_menu(self):
        """rapport menu"""

        choice = self.rapport_view.rapport_menu()

        if choice == "1":
            """list all players in system"""

            if len(Player.table().all()) > 0:
                players_list = Player.rapport()
                self.rapport_view.list_players(players_list)
            else:
                self.rapport_view.list_all_players_response()

            self.rapport_menu()

        elif choice == "2":
            """list all tournaments"""

            if len(Tournament.table().all()) > 0:
                tournaments_list = Tournament.tournaments_rapport()
                self.rapport_view.list_all_tournaments(tournaments_list)
            else:
                self.rapport_view.all_tournaments_response()

            self.rapport_menu()

        elif choice == "3":
            """find a tournament"""

            choice_3 = self.rapport_view.tournament_name()
            if len(Tournament.find(choice_3)) > 0:
                tournament3 = Tournament.load(choice_3)
                tournament_list = tournament3.tournament_rapport()
                self.rapport_view.found_tournament(tournament_list)
            else:
                self.rapport_view.tournament_name_reponse1()

            self.rapport_menu()

        elif choice == "4":
            """list all players of one tournament"""

            choice_4 = self.rapport_view.tournament_name()
            if len(Tournament.find(choice_4)) > 0:
                tournament4 = Tournament.load(choice_4)
                if len(tournament4.players_score) > 0:
                    players_list = tournament4.players_name_rapport()
                    self.rapport_view.list_tournaments_players(players_list)
                else:
                    self.rapport_view.tournament_name_reponse2()
            else:
                self.rapport_view.tournament_name_reponse1()

            self.rapport_menu()

        elif choice == "5":
            """list all matchs and rounds of one tournament"""

            choice_5 = self.rapport_view.tournament_name()
            if len(Tournament.find(choice_5)) > 0:
                tournament5 = Tournament.load(choice_5)
                if tournament5.current_round > 0:
                    rounds_list = tournament5.rounds_rapport()
                    self.rapport_view.list_rounds(rounds_list)
                else:
                    self.rapport_view.list_rounds_response()
            else:
                self.rapport_view.tournament_name_reponse1()

            self.rapport_menu()

        elif choice == "6":
            """Back to Home Menu"""

            return "exit"

        else:
            """invalid choice"""
            self.rapport_view.invalid_choice()
            self.rapport_menu()

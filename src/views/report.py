""" class ReportView"""

from .common import top_bottom, get_choice
from .player import PlayerView
from .tournament import TournamentView


class ReportView:
    @top_bottom
    def menu(self) -> str:
        """display the report menu and get the choice"""

        print("\n                              Report menu\n")
        print("                              1 -- List players")
        print("                              2 -- List tournaments")
        print("                              3 -- Select tournament")
        print("                              4 -- Tournament players")
        print("                              5 -- Tournament rounds")
        print("                              6 -- Back to Home Menu\n")

        return get_choice()

    def list_players(self, players_list: list, action: str, location: str):
        """list players in system"""

        PlayerView().list_players(players_list, action, location)
        if len(players_list) > 0:
            print(
                "\n*A full players report has been exported to the folder : data/exports/\n"
            )
            if location == "system":
                print("as file : system_players_report.xlsx")
            if location == "tournament":
                print(
                    f"as file : tournament_({players_list[0]['tournament']})_players_name_report.xlsx"
                )

    def list_tournaments(self, tournaments_list: list, action: str):
        """list all tournaments"""

        TournamentView().list_tournaments(tournaments_list, action)
        if len(tournaments_list) == 1:
            print(
                "\n*A full tournament report has been exported to the folder : data/exports/\n"
            )
            print(f"as file : tournament_({tournaments_list[0]['name']})_report.xlsx")
        if len(tournaments_list) > 1:
            print(
                "\n*A full tournaments report has been exported to the folder : data/exports/\n"
            )
            print("as file : tournaments_report.xlsx")

    def tournament_name(self) -> str:
        """get the tournament name"""

        print("\nPlease enter the tournament's name now\n")

        return TournamentView()._get_name()

    def tournament_name_reponse(self):
        """used if no found tournament"""

        TournamentView()._inexistent_tournament()

    def list_rounds(self, rounds_list: list):
        """list all rounds and matchs in a tournament"""

        if len(rounds_list) > 0:
            print(
                "\n Match           | Player 1 name    | Player 1 score  | Player 2 score  | Player 2 name    | Round"
            )
            print(
                "_________________|__________________|_________________|_________________|__________________|________"
            )
            for y in rounds_list:
                match = str(y[0]).ljust(15, " ")
                p1_name = y[2].ljust(15, " ")
                p1_score = str(y[3]).ljust(15, " ")
                p2_score = str(y[4]).ljust(15, " ")
                p2_name = y[5].ljust(15, " ")
                round = y[7].ljust(15, " ")
                print(
                    f" {match} | {p1_name} | {p1_score} | {p2_score} | {p2_name} | {round}"
                )
            print(
                "\n*A full rounds report has been exported to the folder : data/exports/\n"
            )
            print(f"as file : rounds_report_of_tournament_({rounds_list[0][11]}).xlsx")
        else:
            print("\n0 round created in this tournament.\n")

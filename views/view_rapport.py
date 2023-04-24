""" Class rapport menu view"""


class ViewRapport:
    """rapport view."""

    def rapport_menu(self):
        """display rapport menu"""

        print("-" * 80)
        print(
            """                          ♟️   Chess Game ♟️ 

                          Rapport Menu
            
                          
            1 -- All players in system
            2 -- List all tournaments
            3 -- Find a tournament
            4 -- All players in tournament
            5 -- All rounds in tournament
            6 -- Back to Home Menu
            
            """
        )
        print("-" * 80)
        print()
        response = input("your choice > ")

        return response

    def list_all_players_response(self):
        """used if no player registered in tournament"""

        print("\n🛑🚫 No player registered in system.\n")

    def all_tournaments_response(self):
        """used if no found created tournament"""

        print("\n🛑🚫 No created tournament in system.\n")

    def tournament_name(self):
        """ask tounament name and return it"""

        response = input("\nenter the tournament name > ")

        return response

    def tournament_name_reponse1(self):
        """used if no tournament found"""

        print(
            "\n🛑🚫 No found tournament with this name, please retry with an existant tournament name.\n"
        )

    def tournament_name_reponse2(self):
        """used if no player registered in tournament"""

        print("\n🛑🚫 No player registered in this tournament.\n")

    def list_rounds_response(self):
        """used if no rounds is running in the tournament"""

        print("\n🛑🚫 No round is running in this tournament.\n")

    def list_players(self, players_list: list):
        """list players in system"""

        print()
        print(" Last-Name       | First-Name      | Ine")
        print("_________________|_________________|________")
        for y in players_list:
            print(f" {y[0].ljust(15,' ')} | {y[1].ljust(15,' ')} | {y[3]}")
        print()
        print("*Full players rapport in system exported to data/exports/\n")
        print("as file : system_players_rapport.xlsx")

    def list_all_tournaments(self, tournaments_list: list):
        """list all tournaments"""

        print()
        print(
            " Name            | Place           | Status          | Start_date      | End_date"
        )
        print(
            "_________________|_________________|_________________|_________________|_________________"
        )
        for y in tournaments_list:
            print(
                f" {y[0].ljust(15,' ')} | {y[1].ljust(15,' ')} | {y[3].ljust(15,' ')} | {y[4].ljust(15,' ')} | {y[5].ljust(15,' ')}"
            )
        print()
        print("*Full tournaments rapport exported to data/exports/\n")
        print("as file : tournaments_rapport.xlsx")

    def found_tournament(self, tournament_list: list):
        """diplay tournament data"""

        print()
        print(
            " Name            | Place           | Status          | Start_date      | End_date"
        )
        print(
            "_________________|_________________|_________________|_________________|_________________"
        )

        print(
            f" {tournament_list[0].ljust(15,' ')} | {tournament_list[1].ljust(15,' ')} | {tournament_list[2].ljust(15,' ')} | {tournament_list[3].ljust(15,' ')} | {tournament_list[4].ljust(15,' ')}"
        )
        print()
        print("*Full tournament rapport exported to data/exports/\n")
        print("as file : tournament_('tournament_name')_rapport.xlsx")

    def list_tournaments_players(self, players_list: list):
        """list_tournaments_players"""

        print()
        print(" Last-Name       | First-Name      | Ine")
        print("_________________|_________________|________")
        for y in players_list:
            print(f" {y[0].ljust(15,' ')} | {y[1].ljust(15,' ')} | {y[3]}")
        print()
        print("*Full players rapport of the tournament exported to data/exports/\n")
        print("as file : tournament_('tournament_name')_players_name_rapport.xlsx")

    def list_rounds(self, rounds_list: list):
        """list all rounds and matchs in a tournament"""

        print()
        print(
            " Match           | Player 1 name    | Player 1 score  | Player 2 score  | Player 2 name    | Round number   "
        )
        print(
            "_________________|__________________|_________________|_________________|__________________|_______________"
        )
        for y in rounds_list:
            print(
                f" {str(y[0]).ljust(15,' ')} | {y[2].ljust(15,' ')} | {str(y[3]).ljust(15,' ')} | {str(y[4]).ljust(15,' ')} | {y[5].ljust(15,' ')} | {y[7].ljust(15,' ')}"
            )
        print()
        print("*Full rounds rapport exported to data/exports/\n")
        print("as file : rounds_rapport_of_tournament_('tournament_name').xlsx")

    def invalid_choice(self):
        """used when invalid choice is selected"""

        print(f"\nInvalide choice !\n ")

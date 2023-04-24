""" Class tournament menu view"""

from pprint import pprint


class ViewTournament:
    """tournament view."""

    def tournament_menu(self, preview: str):
        """display tournament menu"""

        print("-" * 80)
        print(
            f"""                          ♟️   Chess Game ♟️ 

                          Tournament Menu
            
            {preview}              
                          
            1 -- Create
            2 -- Add player
            3 -- Delete player
            2 -- Play
            3 -- Edit place, description
            4 -- Delete
            5 -- Back to Home Menu

            tournament name* must be unique
            tournament name* is deletable but not editable"""
        )
        print("-" * 80)
        print()
        response = input("your choice > ")

        return response

    def create(self) -> list:
        """ask tournaments arguments to create it"""

        print("tournament name* must be unique")
        print("Enter tournament's values now")
        print()
        response1 = input("Tournament's name* > ")
        response2 = input("Tournament's place > ")
        response3 = input("Tournament's description > ")
        response = [response1, response2, response3]

        return response

    def create_response(self, response: bool):
        """used if tournament name isn't unique or to confirm the creation"""

        if response:
            print("\nTournament created successfully !\n")
        else:
            print("\n🛑🚫 Tournament's name is not unique !\n")

    def tournaments_name(self, tournaments_list: list):
        """diplay tournaments list created in the system"""

        if len(tournaments_list) == 0:
            print(f"\n0 tournament created in the system.\n")
        if len(tournaments_list) == 1:
            print(f"\n1 tournament created in the system :\n")
            print(tournaments_list[0])
        if len(tournaments_list) > 1:
            print(f"\n{len(tournaments_list)} tournaments created in the system :\n")
            print(" ___________________")
            print("| tournaments name  |")
            print("|___________________|")
            for t in tournaments_list:
                print(f"| {t}")
            print()
            print("To wich tournament would you like to add players ?")

    def list_players(self, players_list: dict):
        """list players in system"""

        print(f"\n{len(players_list)} players registered in system :\n")
        print(" Last-Name       | First-Name      | Ine")
        print("_________________|_________________|________")
        for y in players_list:
            print(
                f" {y['last_name'].ljust(15,' ')} | {y['first_name'].ljust(15,' ')} | {y['ine']}"
            )
        print()

    def add_player1(self) -> list:
        """get tournament name"""

        response = input("Tournament's name* > ")

        return response

    def add_player2(self, players_list: list):
        """print tournament players list"""

        if len(players_list) == 0:
            print(f"\n0 registered players in this tournament.\n")

        else:
            print(f"\n{len(players_list)} registered players in this tournament :\n")
            print(" Last-Name       | First-Name      | Ine")
            print("_________________|_________________|________")
            for y in players_list:
                print(f" {y[0].ljust(15,' ')} | {y[1].ljust(15,' ')} | {y[3]}")
            print()

    def add_player3(self) -> list:
        """get the number of players to add"""

        response = input("How many players wish you add ? (6 max.)> ")

        return response

    def add_player4(self, number_of_players: int):
        """get players ine"""

        players_ine = []
        i = 1
        for p in range(number_of_players):
            response = input(f"Player {i}'s ine > ")
            players_ine.append(response)
            i += 1

        return players_ine

    def add_player5(
        self, reponse1: bool, reponse2: bool, players_added: int, player_to_add: int
    ) -> list:
        """return the numbre of ine added in tournament"""

        if reponse1 and reponse2:
            print(f"\n{players_added}/{player_to_add} players added successfully !\n")

        elif reponse1 and not reponse2:
            if players_added > 0:
                print(
                    f"\n🛑🚫 Only {players_added}/{player_to_add}  players added successfully ! Check players ine that haven't been added...\n"
                )
                print(
                    "All players ine must exist in the system before they can be added to a tournament.\n"
                )
            if players_added == 0:
                print(
                    f"\n🛑🚫 0/{player_to_add} players added... Please check players ine that haven't been added...\n"
                )
                print(
                    "All players ine must exist in the system before they can be added to a tournament.\n"
                )
        elif not reponse1:
            print("\n🛑🚫 This tournament name does not exist in the system.\n")

    def invalid_choice(self):
        """used when invalid choice is selected"""

        print(f"\nInvalide choice !\n ")

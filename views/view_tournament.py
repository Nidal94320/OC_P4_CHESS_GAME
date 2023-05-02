""" Class tournament menu view"""

from models.matchs import Match


class ViewTournament:
    """tournament view."""

    def tournament_menu(self, preview: str):
        """display tournament menu"""

        print("-" * 80)
        print(
            f"""                          ♟️   Chess Game ♟️ 

                          Tournament Menu
            
            {preview}              
                          
            1 -- List
            2 -- Select
            3 -- Create
            4 -- Edit
            5 -- Delete
            6 -- Back to Home Menu

            tournament name* must be unique
            tournament name* is deletable but not editable"""
        )
        print("-" * 80)
        print()
        response = input("your choice > ")

        return response

    def tournaments_name(self, tournaments_list: list):
        """diplay tournaments list created in the system"""

        if len(tournaments_list) == 0:
            print(f"\n0 tournament created in the system.\n")
        if len(tournaments_list) == 1:
            print(f"\n1 tournament created in the system :\n")
            print(tournaments_list[0])
        if len(tournaments_list) > 1:
            print(f"\n{len(tournaments_list)} tournaments created in the system :\n")
            print(" ________________________________")
            print("|        Tournaments name        |")
            print("|________________________________|")
            for t in tournaments_list:
                print(f"| {t.ljust(30,' ')} |")
            print()

    def create(self) -> list:
        """ask tournament arguments to create it"""

        print("\nTournament name* must be unique.\n")
        print("Please enter the tournament's values now :")
        print()
        response1 = input("Tournament's name* > ")
        response2 = input("Tournament's place > ")
        response3 = input("Tournament's description > ")
        response = [response1, response2, response3]

        return response

    def create_response1(self):
        """used if the number of players registered in system < 4"""

        print(
            "\n🛑🚫 It is necessary to have a minimum of 4 players registered in system !\n"
        )
        print(
            "Please go to players menu to create players in system to be able to add them in the tournament.\n"
        )

    def create_response2(self, response1: bool, response2: bool):
        """used if tournament name isn't unique or to confirm the creation"""

        if response1 and response2:
            print("\n🟢 Tournament created successfully !\n")

        if response1 and not response2:
            print(
                "\n🛑🚫 A minimum of 4 valid player ine's is required to create a tournament.\n"
            )
            print("\nPlease retry with correct values.\n")
        if not response1 and not response2:
            print("\n🛑🚫 Tournament's name is not unique !\n")
            print("\nPlease try again with a different tournament name.\n")

    def list_players(self, players_list: dict):
        """list players in system"""

        print("\nHere is the list of players registered in the system :\n")
        print(" Last-Name       | First-Name      | Ine")
        print("_________________|_________________|________")
        for y in players_list:
            print(
                f" {y['last_name'].ljust(15,' ')} | {y['first_name'].ljust(15,' ')} | {y['ine']}"
            )
        print()

    def add_player1(self, number_of_players: int) -> list:
        """get the number of players to add"""

        print("\nA minimum of 4 players is required to create a tournament.")
        print(
            f"\nBut don't exceed the number of players in the system, which is {number_of_players}.\n"
        )
        response = input("How many players would you like to add ? (4 min.)> ")

        return response

    def add_player2(self, number_of_players: int):
        """get players ine list"""

        players_ine = []
        i = 1
        for p in range(number_of_players):
            response = input(f"Player {i}'s ine > ")
            players_ine.append(response)
            i += 1

        return players_ine

    def add_player_response1(self):
        """used if the number of players entered by the user is incorrect"""

        print("\n🛑🚫 Incorrect value !\n")

    def add_player_response2(
        self, reponse1: bool, reponse2: bool, players_added: int, player_to_add: int
    ) -> list:
        """return the numbre of ine added in tournament"""

        if reponse1 and reponse2:
            print(f"\n🟢 {players_added}/{player_to_add} players added successfully !\n")

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

    def edit(self) -> list:
        """ask tournaments arguments to edit it"""

        print("\nWhich tournament would you like to edit ?\n")
        response1 = input("Tournament's name* > ")
        print("\nPlease enter the tournament's new values now :\n")
        response2 = input("Tournament's place > ")
        response3 = input("Tournament's description > ")

        return [response1, response2, response3]

    def edit_response(self, response: bool):
        """display response"""

        if response:
            print("\n 🟢 Tournament edited successfully !\n")
        else:
            print("\n 🛑🚫 Invalid tournament's name !\n")
            print("Please try again with a registered tournament name.\n")

        return response

    def delete(self) -> str:
        """ask tournaments arguments to edit it"""

        print("\nWhich tournament would you like to delete ?\n")
        print("🟠 The tournament's data will be definitevely lost...\n")

        response = input("Tournament's name* > ")

        return response

    def delete_response1(self) -> str:
        """ask the deletion's confirmation"""

        print("\nDo you confirm the deletion ?\n")

        response = input("y/n > ")

        return response

    def delete_response2(self):
        """the deletion's confirmation"""

        print("\n 🟢 Tournament deleted successfully !\n")

    def select1(self) -> str:
        """ask tournament name"""

        print("\nThe tournament must be created in the system.\n")
        print("\nWhich tournament would you like to select ?\n")
        response = input("Tournament's name* > ")

        return response

    def select_round(self, tournament_data: list, player_ranking: list,current_round:int):
        """display the tournament's data when the current round is finished
        or when the tournament status is 'created'"""

        print()
        print("-" * 80)
        print()
        print(" __________________________________________________________________")
        print("| Tournament name                | Status         | Current round  |")
        print("|________________________________|________________|________________|")
        print("|                                |                |                |")

        print(
            f"| {tournament_data[0].ljust(30,' ')} | {tournament_data[1].ljust(14,' ')} | {tournament_data[2].ljust(14,' ')} |"
        )
        print("|________________________________|________________|________________|\n")

        for p in player_ranking:
            print(f" {str(p[0])}  {p[2].ljust(10,' ')} {p[1]} pt")
        print()
        if current_round>0:
            print(f"The round {current_round} is finished.\n")
        print("Would you like to run the next round?\n")
        response = input("y/n > \n")

        return response

    def select_end(self, tournament_data: list, player_ranking: list):
        """display the tournament's data when it has conclued"""

        print()
        print("-" * 80)
        print()
        print(" __________________________________________________________________")
        print("| Tournament name                | Status         | Current round  |")
        print("|________________________________|________________|________________|")
        print("|                                |                |                |")

        print(
            f"| {tournament_data[0].ljust(30,' ')} | {tournament_data[1].ljust(14,' ')} | {tournament_data[2].ljust(14,' ')} |"
        )
        print("|________________________________|________________|________________|\n")

        j = 1
        for p in player_ranking:
            if j == 1:
                print(f" {str(p[0])}  {p[2].ljust(10,' ')} {p[1]} pt 🥇")
                j += 1
                continue
            elif j == 2:
                print(f" {str(p[0])}  {p[2].ljust(10,' ')} {p[1]} pt 🥈")
                j += 1
                continue
            elif j == 3:
                print(f" {str(p[0])}  {p[2].ljust(10,' ')} {p[1]} pt 🥉")
                j += 1
                continue
            else:
                print(f" {str(p[0])}  {p[2].ljust(10,' ')} {p[1]} pt")
                j += 1

    def select_match(
        self, tournament_data: list, player_ranking: list, match_list: list
    ):
        """display the tournament's data when the current round is ruuning"""

        print()
        print("-" * 80)
        print()
        print(" __________________________________________________________________")
        print("| Tournament name                | Status         | Current round  |")
        print("|________________________________|________________|________________|")
        print("|                                |                |                |")

        print(
            f"| {tournament_data[0].ljust(30,' ')} | {tournament_data[1].ljust(14,' ')} | {tournament_data[2].ljust(14,' ')} |"
        )
        print("|________________________________|________________|________________|\n")

        for p in player_ranking:
            print(f" {str(p[0])}  {p[2].ljust(10,' ')} {p[1]} pt")
        print()

        i = 1
        for m in match_list:
            print(Match(i, m))
            i += 1

        print("Would you like to enter the result of a match ?\n")
        response = input("y/n > \n")

        return response

    def select_result(self) -> list:
        """get the match result"""

        print("\nThe winner gets 1 point and the loser gets 0 point,")
        print("both players get 0.5 point if they draw.")
        print("\nFor wich match would you like to enter the result ?\n")

        response1 = input("\nThe match number (ex : 1) > ")
        response2 = input("The score of the player in white (ex : 1) > ")
        response3 = input("The score of the player in black (ex : 0) > ")

        return [response1, response2, response3]

    def select_result_response(self, response1: bool, response2: bool) -> list:
        """get the match result"""

        if response1 and response2:
            print("\n 🟢 Match updated successfully !\n")
        if response1 and not response2:
            print("\n🛑🚫 Invalid result entered !\n")
            print("\nPlease try again with a valid result")
        if not response1:
            print("\n🛑🚫 Invalid match number !\n")
            print("\nPlease try again with a valid match number")

    def invalid_choice(self):
        """used when invalid choice is selected"""

        print(f"\n🛑🚫 Invalide choice !\n ")
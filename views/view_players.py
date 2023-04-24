"""Class viewplayers"""


class ViewPlayers:
    """players menu view"""

    def player_menu(self, preview: str) -> str:
        """display player menu"""

        print("-" * 80)
        print(
            f"""                          ♟️   Chess Game ♟️ 

                          Player Menu
            
            {preview}
                          
            1 -- List
            2 -- Create
            3 -- Find
            4 -- Edit
            5 -- Delete
            6 -- Back to Home Menu

            ine* is the National Chess ID and, it must be unique
            ine* is deletable but not editable"""
        )
        print("-" * 80)
        print()
        response = input("your choice > ")

        return response

    def add_player(self) -> list:
        """create a new player in database"""

        print("Enter player's values now")
        print("ine* is unique to each players")
        print()
        response1 = input("Player's last-name > ")
        response2 = input("Player's first-name > ")
        response3 = input("Player's birthdate > ")
        response4 = input("Player's ine* > ")
        response = [response1, response2, response3, response4]

        return response

    def response_add(self, response: bool) -> None:
        """print response after adding a player"""

        print()
        if response:
            print("player registered successfully !")
        else:
            print("ine* is already in system or in incorrect format !")
            print("Please retry with another valid ine*")
        print()

    def find_player(self) -> str:
        """find a player in database by its ine"""

        response = input("Player's ine* > ")

        return response

    def response_find(self, result: list) -> None:
        """print found player if result"""

        print()
        if (len(result)) == 0:
            print(f"\n{len(result)} player found in system.\n ")

        elif (len(result)) == 1:
            print(f"\n{len(result)} player found in system :\n ")

        elif len(result) > 1:
            print(f"\n{len(result)} players found in system :\n ")

        if len(result) > 0:
            print("Last-Name       - First-Name      - Birthdate       - ine\n")
            for p in result:
                print(
                    f"{p['last_name'].ljust(15,' ')} - {p['first_name'].ljust(15,' ')} - {p['birthdate'].ljust(15,' ')} - {p['ine']}"
                )

    def edit_player(self) -> list:
        """Edit player in database"""

        print()
        print("Enter player's ine* to edit")
        print()

        response4 = input("Player's ine* > ")
        print()
        print("Please enter the new player's values now")
        print()
        response1 = input("Player's last-name > ")
        response2 = input("Player's first-name > ")
        response3 = input("Player's birthdate > ")
        response = [response1, response2, response3, response4]

        return response

    def response_edit(self, response: bool) -> None:
        """print response after adding a player"""

        print()
        if response:
            print("player edited successfully !")
        else:
            print("ine* not found in system ! Please retry with registered ine*")
        print()

    def delete(self) -> str:
        """delete player from databse by its ine"""

        print()
        print("Enter player's ine* to delete from system")
        print()
        response = input("Player's ine* > ")

        return response

    def reponse_delete(self, response: bool) -> None:
        """print response after deleting a player"""

        print()
        if response:
            print("player deleted successfully !")
        else:
            print("ine* not found in system ! Please retry with registered ine*")
        print()

    def list_players(self, result: list) -> None:
        """print players list sorted by name"""

        if len(result) > 1:
            print(f"\n{len(result)} joueurs enregistrés dans le système :\n ")
        else:
            print(f"\n{len(result)} joueur enregistré dans le système :\n ")
        print("\nLast-Name       - First-Name      - Birthdate       - ine \n")
        for p in result:
            print(
                f"{p['last_name'].ljust(15,' ')} - {p['first_name'].ljust(15,' ')} - {p['birthdate'].ljust(15,' ')} - {p['ine']}"
            )

    def invalid_choice(self):
        """used when invalid choice is selected"""

        print(f"\nInvalide choice !\n ")

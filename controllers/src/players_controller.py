"""Players Menu controller"""

import re

from models.players import Player
from views.view_players import ViewPlayers


class PlayersController:
    def __init__(self):
        self.view_players = ViewPlayers()

    def players_menu(self):
        # players_menu
        if len(Player.read_all()) < 2:
            preview = str(len(Player.read_all())) + " player registered in system."
        else:
            preview = str(len(Player.read_all())) + " players registered in system."
        choice = self.view_players.player_menu(preview)

        if choice == "1":
            """1. diplay players list"""

            self.view_players.list_players(Player.read_all())
            # sleep(5)
            # return to Players menu
            self.players_menu()

        elif choice == "2":
            """2. select a player by its ine"""

            choice_2 = self.view_players.find_player().upper().strip()
            self.view_players.response_find(Player.find_player(choice_2))
            # sleep(5)
            # return to Players menu
            self.players_menu()

        elif choice == "3":
            """3. create a new player"""

            choice_3 = self.view_players.add_player()
            if (len(choice_3[3]) == 7) and (
                len(
                    Player.find_player(
                        re.sub(r"[^\w\s-]+", "", choice_3[3])
                        .lower()
                        .replace("é", "e")
                        .replace("è", "e")
                        .replace("à", "a")
                        .replace("ç", "c")
                        .upper()
                        .strip()
                    )
                )
                == 0
            ):
                Player(
                    re.sub(r"[^\w\s-]+", "", choice_3[0])
                    .lower()
                    .replace("é", "e")
                    .replace("è", "e")
                    .replace("à", "a")
                    .replace("ç", "c")
                    .upper()
                    .strip(),
                    re.sub(r"[^\w\s-]+", "", choice_3[1])
                    .lower()
                    .replace("é", "e")
                    .replace("è", "e")
                    .replace("à", "a")
                    .replace("ç", "c")
                    .capitalize()
                    .strip(),
                    choice_3[2]
                    .lower()
                    .replace("é", "e")
                    .replace("è", "e")
                    .replace("à", "a")
                    .replace("ç", "c")
                    .upper()
                    .strip(),
                    re.sub(r"[^\w\s-]+", "", choice_3[3])
                    .lower()
                    .replace("é", "e")
                    .replace("è", "e")
                    .replace("à", "a")
                    .replace("ç", "c")
                    .upper()
                    .strip(),
                ).create()

                response = True
            else:
                response = False

            self.view_players.response_add(response)

            # return to Players menu
            self.players_menu()

        elif choice == "4":
            """4. edit player by ine"""

            choice_4 = self.view_players.edit_player()
            if len(Player.find_player(choice_4[3])) == 1:
                p = Player.load(choice_4[3])
                p.last_name = choice_4[0].upper().strip()
                p.first_name = choice_4[1].capitalize().strip()
                p.birthdate = choice_4[2].upper().strip()
                p.update()
                response = True
            else:
                response = False
            self.view_players.response_edit(response)
            # return to Players menu
            self.players_menu()

        elif choice == "5":
            """5. delete player"""

            choice_5 = self.view_players.delete().upper()
            if len(Player.find_player(choice_5)) == 1:
                Player.load(choice_5).delete()
                response = True
            else:
                response = False
            self.view_players.reponse_delete(response)
            # return to Players menu
            self.players_menu()

        elif choice == "6":
            """6. Return to Home menu"""

            return "exit"

        else:
            """return to Players menu if invalid choice"""

            self.view_players.invalid_choice()
            self.players_menu()

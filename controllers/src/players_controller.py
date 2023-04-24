"""Players Menu controller"""


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
            # 1. diplay players list
            self.view_players.list_players(Player.read_all())
            # sleep(5)
            # return to Players menu
            self.players_menu()

        elif choice == "2":
            # 2. add a new player menu
            choice_2 = self.view_players.add_player()
            if (len(choice_2[3]) == 7) and (len(Player.find_player(choice_2[3])) == 0):
                Player(
                    choice_2[0].upper().strip(),
                    choice_2[1].capitalize().strip(),
                    choice_2[2].upper().strip(),
                    choice_2[3].upper().strip(),
                ).create()

                response = True
            else:
                response = False

            self.view_players.response_add(response)

            # return to Players menu
            self.players_menu()

        elif choice == "3":
            # 3. find a player by its ine
            choice_3 = self.view_players.find_player().upper().strip()
            self.view_players.response_find(Player.find_player(choice_3))
            # sleep(5)
            # return to Players menu
            self.players_menu()

        elif choice == "4":
            # 4. edit player by ine
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
            # 5. delete player
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
            # 6. Return to Home menu
            return "exit"

        else:
            # return to Players menu if invalid choice
            self.view_players.invalid_choice()
            self.players_menu()

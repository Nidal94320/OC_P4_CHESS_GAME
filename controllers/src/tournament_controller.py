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

        if len(Tournament.tournaments_name()) < 2:
            preview = (
                str(len(Tournament.tournaments_name()))
                + " tournament created in system."
            )
        else:
            preview = (
                str(len(Tournament.tournaments_name()))
                + " tournaments created in system."
            )

        choice = self.tournament_view.tournament_menu(preview)

        if choice == "1":
            """create"""

            choice_1 = self.tournament_view.create()
            if choice_1[0].upper().strip() not in Tournament.tournaments_name():
                tournament = Tournament(
                    choice_1[0].upper().strip(),
                    choice_1[1].upper().strip(),
                )
                tournament.description = choice_1[2].upper().strip()
                tournament.create()
                self.tournament_view.create_response(True)
            else:
                self.tournament_view.create_response(False)

            self.tournament_menu()

        elif choice == "2":
            """add player"""

            self.tournament_view.tournaments_name(Tournament.tournaments_name())
            # on vérifie l'exitence du tournoi et on charge l'instance
            choice_2_1 = self.tournament_view.add_player1()
            if choice_2_1.upper().strip() in Tournament.tournaments_name():
                tournament = Tournament.load(choice_2_1.upper().strip())

                # on charge la liste des joueurs du tournoi et on l'affiche
                players = tournament.tournament_players()
                self.tournament_view.add_player2(players)

                # on récupere le nombre de joueur à ajouter et on le vérifie
                choice_2_3 = self.tournament_view.add_player3()

                self.tournament_view.list_players(Player.read_all())

                if choice_2_3.upper().strip().isdigit():
                    if int(choice_2_3.upper().strip()) < 7:
                        # on récupère autant d'ine que demandé à l'étape 3
                        choice_2_4 = self.tournament_view.add_player4(
                            int(choice_2_3.upper().strip())
                        )

                        added_players = tournament.add_players_list(choice_2_4)

                        if added_players == int(choice_2_3.upper().strip()):
                            self.tournament_view.add_player5(
                                True,
                                True,
                                added_players,
                                int(choice_2_3.upper().strip()),
                            )
                        elif added_players < int(choice_2_3.upper().strip()):
                            self.tournament_view.add_player5(
                                True,
                                False,
                                added_players,
                                int(choice_2_3.upper().strip()),
                            )
            else:
                self.tournament_view.add_player5(False, False, 0)

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

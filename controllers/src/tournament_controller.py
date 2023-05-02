"""Tournament Menu controller"""

import re

from views.view_tournament import ViewTournament
from models.players import Player
from models.tournaments import Tournament
from models.rounds import SCORE


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
            """list"""

            self.tournament_view.tournaments_name(Tournament.tournaments_name())
            self.tournament_menu()

        elif choice == "2":
            """select"""

            choice_2_1 = self.tournament_view.select1()
            if (
                re.sub(r"[^\w\s-]+", "", choice_2_1)
                .replace(" ", "_")
                .lower()
                .replace("é", "e")
                .replace("è", "e")
                .replace("à", "a")
                .replace("ç", "c")
                .upper()
                .strip()
                in Tournament.tournaments_name()
            ):

                running = True
                while running:
                    tournament2 = Tournament.load(
                        re.sub(r"[^\w\s-]+", "", choice_2_1)
                        .replace(" ", "_")
                        .lower()
                        .replace("é", "e")
                        .replace("è", "e")
                        .replace("à", "a")
                        .replace("ç", "c")
                        .upper()
                        .strip()
                    )

                    """next round"""

                    if tournament2.rounds_status() and tournament2.status != "finished":
                        choice_2_2 = self.tournament_view.select_round(
                            [
                            tournament2.name,
                            tournament2.status,
                            str(tournament2.current_round)
                            + "/"
                            + str(tournament2.number_of_rounds),
                            ],
                            tournament2.full_player_ranking(),tournament2.current_round
                        )
                        if choice_2_2.lower().strip() == "y":
                            tournament2.draw_round()
                        else:
                            running = False

                    """ update match result """

                    if (
                        not tournament2.rounds_status()
                        and tournament2.status != "finished"
                    ):
                        choice_2_3 = self.tournament_view.select_match(
                            [
                            tournament2.name,
                            tournament2.status,
                            str(tournament2.current_round)
                            + "/"
                            + str(tournament2.number_of_rounds),
                            ],
                            tournament2.full_player_ranking(),
                            tournament2.get_matchs_list(),
                        )
                        if choice_2_3.lower().strip() == "y":
                            choice_2_4 = self.tournament_view.select_result()
                            if choice_2_4[0].isdigit():
                                if (0< int(choice_2_4[0])<= len(tournament2.get_matchs_list())):
                                    if (choice_2_4[1].replace(".","").isdigit() and choice_2_4[2].replace(".","").isdigit()): 
                                        if (float(choice_2_4[1]) in SCORE) and (float(choice_2_4[2]) in SCORE) and (float(choice_2_4[1])+float(choice_2_4[2])==1):
                                            
                                            if float(choice_2_4[1])==0.0 or float(choice_2_4[1])==1.0:
                                                choice_2_4[1]=int(choice_2_4[1])
                                            else:
                                                choice_2_4[1]=0.5

                                            if float(choice_2_4[2])==0.0 or float(choice_2_4[2])==1.0:
                                                choice_2_4[2]=int(choice_2_4[2])
                                            else:
                                                choice_2_4[2]=0.5

                                            tournament2.update_match_result(int(choice_2_4[0])-1,choice_2_4[1],choice_2_4[2])
                                        else:
                                            self.tournament_view.select_result_response(True, False)
                                    else:
                                        self.tournament_view.select_result_response(True, False)
                                else:
                                    self.tournament_view.select_result_response(False,False)
                            else:
                                self.tournament_view.select_result_response(False,False)

                        else:
                            running = False
                    
                    """ finished tournament """

                    if tournament2.status=="finished":
                        self.tournament_view.select_end(
                            [
                            tournament2.name,
                            tournament2.status,
                            str(tournament2.current_round)
                            + "/"
                            + str(tournament2.number_of_rounds),
                            ],
                            tournament2.full_player_ranking()
                        )
                        
                        running=False
                    tournament2.update_players_score()



            else:
                self.tournament_view.edit_response(False)

            self.tournament_menu()

        elif choice == "3":
            """create"""

            if len(Player.read_all()) >= 4:
                choice_3_1 = self.tournament_view.create()
                if (
                    re.sub(r"[^\w\s-]+", "", choice_3_1[0])
                    .replace(" ", "_")
                    .lower()
                    .replace("é", "e")
                    .replace("è", "e")
                    .replace("à", "a")
                    .replace("ç", "c")
                    .upper()
                    .strip()
                    not in Tournament.tournaments_name()
                ):
                    tournament = Tournament(
                        re.sub(r"[^\w\s-]+", "", choice_3_1[0])
                        .replace(" ", "_")
                        .lower()
                        .replace("é", "e")
                        .replace("è", "e")
                        .replace("à", "a")
                        .replace("ç", "c")
                        .upper()
                        .strip(),
                        re.sub(r"[^\w\s-]+", "", choice_3_1[1])
                        .replace(" ", "_")
                        .lower()
                        .replace("é", "e")
                        .replace("è", "e")
                        .replace("à", "a")
                        .replace("ç", "c")
                        .upper()
                        .strip(),
                    )
                    tournament.description = (
                        re.sub(r"[^\w\s-]+", "", choice_3_1[2])
                        .lower()
                        .strip()
                        .replace(" ", "_")
                        .replace("é", "e")
                        .replace("è", "e")
                        .replace("à", "a")
                        .replace("ç", "c")
                    )

                    # on demande combien de joueur on veut ajouter
                    choice_3_2 = self.tournament_view.add_player1(
                        len(Player.read_all())
                    )

                    if choice_3_2.upper().strip().isdigit() and (
                        4 <= int(choice_3_2.upper().strip()) <= len(Player.read_all())
                    ):
                        self.tournament_view.list_players(Player.read_all())

                        # on demande autant d'ine que l'utiliseur en a demandé à choice_2_2
                        choice_3_3 = self.tournament_view.add_player2(
                            int(choice_3_2.upper().strip())
                        )

                        added_players = tournament.add_players_list(
                            list(set(choice_3_3))
                        )
                        if added_players >= 4:
                            if added_players == int(choice_3_2.upper().strip()):
                                self.tournament_view.add_player_response2(
                                    True,
                                    True,
                                    added_players,
                                    int(choice_3_2.upper().strip()),
                                )
                            elif added_players < int(choice_3_2.upper().strip()):
                                self.tournament_view.add_player_response2(
                                    True,
                                    False,
                                    added_players,
                                    int(choice_3_2.upper().strip()),
                                )
                            tournament.rounds_list = []
                            tournament.create()
                            self.tournament_view.create_response2(True, True)
                        else:
                            self.tournament_view.create_response2(True, False)

                    else:
                        self.tournament_view.add_player_response1()

                else:
                    self.tournament_view.create_response2(False, False)

            else:
                self.tournament_view.create_response1()

            self.tournament_menu()

        elif choice == "4":
            """edit"""

            choice_4_1 = self.tournament_view.edit()
            if (
                re.sub(r"[^\w\s-]+", "", choice_4_1[0])
                .replace(" ", "_")
                .lower()
                .replace("é", "e")
                .replace("è", "e")
                .replace("à", "a")
                .replace("ç", "c")
                .upper()
                .strip()
                in Tournament.tournaments_name()
            ):
                tournament4 = Tournament.load(
                    re.sub(r"[^\w\s-]+", "", choice_4_1[0])
                    .replace(" ", "_")
                    .lower()
                    .replace("é", "e")
                    .replace("è", "e")
                    .replace("à", "a")
                    .replace("ç", "c")
                    .upper()
                    .strip()
                )
                tournament4.place = (
                    re.sub(r"[^\w\s-]+", "", choice_4_1[1])
                    .replace(" ", "_")
                    .lower()
                    .replace("é", "e")
                    .replace("è", "e")
                    .replace("à", "a")
                    .replace("ç", "c")
                    .upper()
                    .strip()
                )
                tournament4.description = (
                    re.sub(r"[^\w\s-]+", "", choice_4_1[2])
                    .replace(" ", "_")
                    .lower()
                    .replace("é", "e")
                    .replace("è", "e")
                    .replace("à", "a")
                    .replace("ç", "c")
                    .strip()
                )
                tournament4.update()
                self.tournament_view.edit_response(True)
            else:
                self.tournament_view.edit_response(False)

            self.tournament_menu()

        elif choice == "5":
            """delete"""

            choice_5_1 = self.tournament_view.delete()
            if (
                re.sub(r"[^\w\s-]+", "", choice_5_1)
                .replace(" ", "_")
                .lower()
                .replace("é", "e")
                .replace("è", "e")
                .replace("à", "a")
                .replace("ç", "c")
                .upper()
                .strip()
                in Tournament.tournaments_name()
            ):
                choice_5_2 = self.tournament_view.delete_response1()

                if choice_5_2.strip().lower() == "y":
                    tournament5 = Tournament.load(
                        re.sub(r"[^\w\s-]+", "", choice_5_1)
                        .replace(" ", "_")
                        .lower()
                        .replace("é", "e")
                        .replace("è", "e")
                        .replace("à", "a")
                        .replace("ç", "c")
                        .upper()
                        .strip()
                    )
                    tournament5.delete()
                    self.tournament_view.delete_response2()

            else:
                self.tournament_view.edit_response(False)

            self.tournament_menu()

        elif choice == "6":
            """Back to Home Menu"""

            return "exit"

        else:
            """invalid choice"""

            self.tournament_view.invalid_choice()
            self.tournament_menu()

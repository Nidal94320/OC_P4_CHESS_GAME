""" class tournament """

from random import shuffle
from itertools import combinations

from tinydb import TinyDB, where
import pandas

from models.players import Player
from models.rounds import Round, timestamp


SCORE = [0, 0.5, 1]


class Tournament:
    """Class tournament"""

    def __init__(
        self,
        name: str,
        place: str,
        start_date=timestamp(),
        end_date="(not finished)",
        status="ongoing",
        description="",
        players_score={},
        number_of_rounds=4,
        current_round=0,
        rounds_list=[],
    ):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.description = description
        self.players_score = players_score
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.rounds_list = rounds_list

    def __str__(self):
        """used in print"""

        return f"{self.__dict__}"

    def __repr__(self):
        """used in print"""

        return str(self)

    @classmethod
    def db(self):
        """Create a JSON file as database"""

        return TinyDB("./data/tournaments/tournaments.json")

    @classmethod
    def table(self):
        """Create 'Tournaments' table in database"""

        return self.db().table("Tournaments")

    def create(self):
        """Create a new tournament in Tournaments table"""

        self.table().insert(self.__dict__)

    @classmethod
    def find(self, tournament_name: str) -> list:
        """Look for a tournament in table by its name

        Take as argument a tournament_name(str)

        return found result list"""
        try:
            return self.table().search(where("name") == tournament_name)[0]
        except IndexError:
            return []
        # if len(self.table().search(where("name") == tournament_name)[0]) == 10:
        #     return self.table().search(where("name") == tournament_name)[0]
        # else:
        #     return []

    @classmethod
    def load(self, tournament_name: str):
        """load instance from json"""

        if len(self.find(tournament_name)) == 10:
            tournament = self.find(tournament_name)

            return Tournament(
                tournament["name"],
                tournament["place"],
                tournament["start_date"],
                tournament["end_date"],
                tournament["status"],
                tournament["description"],
                tournament["players_score"],
                tournament["number_of_rounds"],
                tournament["current_round"],
                tournament["rounds_list"],
            )
        else:
            return []

    def update(self):
        """update tournament data in json
        (only tournament.name can't be updated)"""

        self.table().update(
            {
                "place": self.place,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "status": self.status,
                "description": self.description,
                "players_score": self.players_score,
                "number_of_rounds": self.number_of_rounds,
                "current_round": self.current_round,
                "rounds_list": self.rounds_list,
            },
            where("name") == self.name,
        )

    def delete(self):
        """delete a tournament and its rounds from tables(json)"""

        rounds_list = self.rounds_list
        for round_name in rounds_list:
            round = Round.load(round_name)
            round.delete()
        self.table().remove(where("name") == self.name)

    @classmethod
    def tournaments_name(self) -> list:
        """return tournaments name list"""

        tournaments_name = []
        for tournament in Tournament.table().all():
            tournaments_name.append(tournament["name"])

        return tournaments_name

    def tournament_players(self) -> list:
        """return tournament players list"""

        players = []
        for player in list(self.players_score.keys()):
            p = Player.find_player(player)
            players.append(
                [
                    p[0]["last_name"],
                    p[0]["first_name"],
                    p[0]["birthdate"],
                    p[0]["ine"],
                    self.name,
                    self.status,
                    self.current_round,
                ]
            )
        players = sorted(players, key=lambda p: (p[0]))

        return players

    def add_players_list(self, players_ine: list) -> int:
        """add a player to tournament in instance and database"""

        added_players = 0
        for ine in players_ine:
            if ine in Player.players_ine():
                if ine not in list(self.players_score.keys()):
                    self.players_score[ine] = 0
                    added_players += 1

        self.update()

        return added_players

    def first_round(self):
        """generate first round from shuffled players list"""

        players = list(self.players_score.keys())
        shuffle(players)
        number_of_match = len(players) // 2
        round = Round(
            self.name,
            self.name + "_round_" + str(self.current_round + 1),
            self.current_round + 1,
        )
        self.current_round += 1
        self.rounds_list.append(round.name)

        for i in range(number_of_match):
            match = ([players[i], ""], [players[i + 1], ""])
            round.match_list.append(match)

            """supprimer le premier élément de la liste >
            i skip le nouveau premier élément au prochain tour >
            comme ceci le premier couple de joueur de la liste n'apparait plus dans duel """
            players.pop(0)

        round.create()
        self.update()

    def update_match_score(
        self,
        index_of_match: int,
        player1_score: float,
        player2_score: float,
        index_of_round=-1,
    ):
        """update match score of one round (update the last round if no present value)"""

        name_round = self.rounds_list[index_of_round]
        round = Round.load(name_round)
        # print(round.match_list)
        round.match_list[index_of_match][0][1] = player1_score
        round.match_list[index_of_match][1][1] = player2_score
        # print(round.match_list)
        round.update()
        self.round_status(index_of_round)

    def round_status(self, index_of_round=-1) -> bool:
        """check round status and update (update the last round if no present value)

        return a boolean: True for a finished round, False for an ongoing round"""

        name_round = self.rounds_list[index_of_round]
        round = Round.load(name_round)

        finished = True
        for match in round.match_list:
            if (match[0][1] not in SCORE) or (match[1][1] not in SCORE):
                finished = False
        if finished:
            round.end_date = timestamp()
            round.status = "finished"
        else:
            round.end_date = ""
            round.status = "ongoing"

        round.update()

        return finished

    def all_round_status(self) -> bool:
        """check if all created rounds of the tournament are finished

        return a boolean: True if all round are finished, False for the reverse"""

        finished = True
        rounds_list = self.rounds_list
        for r in rounds_list:
            round = Round.load(r)
            if round.status != "finished":
                finished = False

        return finished

    def update_players_score(self):
        """update players score and update database"""

        if self.all_round_status():
            players_score = []
            for p in list(self.players_score.keys()):
                players_score.append([p, 0])
            rounds_list = self.rounds_list

            for round_id in rounds_list:
                round = Round.load(round_id)
                for match in round.match_list:
                    for player in players_score:
                        if match[0][0] == player[0]:
                            player[1] += match[0][1]
                        if match[1][0] == player[0]:
                            player[1] += match[1][1]

            for ine in players_score:
                self.players_score[ine[0]] = ine[1]

            self.update()

    def delete_last_round(self):
        """delete the last round"""

        self.current_round -= 1
        last_round_name = self.rounds_list[-1]
        self.rounds_list.pop(-1)
        last_round = Round.load(last_round_name)
        last_round.delete()
        self.update()
        self.update_players_score()

    def played_matchs(self) -> list:
        """generate a list of played matchs"""

        played_matchs = []
        rounds_list = self.rounds_list
        players = self.players_rank()
        for player in players:
            played_matchs.append((player, player))

        for round_id in rounds_list:
            round = Round.load(round_id)
            for match in round.match_list:
                played_matchs.append((match[0][0], match[1][0]))
                played_matchs.append((match[1][0], match[0][0]))

        return played_matchs

    def players_rank(self) -> list:
        """generate players list sorted by rank"""

        players = []
        for p in sorted(list(self.players_score.items()), key=lambda p: (-p[1])):
            players.append(p[0])

        return players

    def next_round(self):
        """generate a next round based on players rank played matchs"""

        played_matchs = self.played_matchs()
        players = self.players_rank()
        match_list = []
        participants = []

        i = 1
        for player1 in players[:-1]:
            for player2 in players:
                match = (player1, player2)
                # on vérifie que le match ne soit pas déjà joué dans les rounds précédents (played_matchs)
                if match not in played_matchs:
                    # on vérifie que les joueurs du match ne sont pas déjà présent dans match_list
                    if player1 not in participants:
                        if player2 not in participants:
                            match_list.append(([player1, ""], [player2, ""]))
                            participants.append(player1)
                            participants.append(player2)
            i = i + 1

        round = Round(
            self.name,
            self.name + "_round_" + str(self.current_round + 1),
            self.current_round + 1,
        )
        round.match_list = match_list
        self.current_round += 1
        self.rounds_list.append(round.name)

        round.create()
        self.update()

    def next_round_2(self):
        """generate a next round based on players rank played matchs"""

        played_matchs = self.played_matchs()
        players = self.players_rank()
        match_list = []
        participants = []
        all_matchs = []
        for p in combinations(players, 2):
            all_matchs.append(p)

        for match in all_matchs:
            if match not in played_matchs:
                if match[0] not in participants:
                    if match[1] not in participants:
                        match_list.append(([match[0], ""], [match[1], ""]))
                        participants.append(match[0])
                        participants.append(match[1])

        round = Round(
            self.name,
            self.name + "_round_" + str(self.current_round + 1),
            self.current_round + 1,
        )
        round.match_list = match_list
        self.current_round += 1
        self.rounds_list.append(round.name)

        round.create()
        self.update()

    """ rapport methode """

    def players_rank_rapport(self):
        """export a players rank rapport (.xlsx) and print a preview of it"""

        players_rank = []
        players = self.players_rank()

        i = 1
        for player in players:
            p = Player.find_player(player)
            s = [
                i,
                self.players_score[player],
                p[0]["last_name"],
                p[0]["first_name"],
                p[0]["ine"],
                self.name,
                self.status,
                self.current_round,
            ]
            players_rank.append(s)
            i += 1

        data = [
            {
                "rank": r[0],
                "score": r[1],
                "last_name": r[2],
                "first_name": r[3],
                "ine": r[4],
                "tournament": self.name,
                "status": self.status,
                "round": self.current_round,
            }
            for r in players_rank
        ]
        data_to_export = pandas.DataFrame.from_records(data)
        file_path = (
            "./data/exports/tournament_(" + self.name + ")_players_rank_rapport.xlsx"
        )
        data_to_export.to_excel(file_path)
        print()
        print(" Rank       | Score      | Last-Name       | First-Name      | Ine")
        print(
            "____________|____________|_________________|_________________|____________"
        )
        for y in players_rank:
            print(
                f" {str(y[0]).ljust(10,' ')} | {str(y[1]).ljust(10,' ')} | {y[2].ljust(15,' ')} | {y[3].ljust(15,' ')} | {y[4].ljust(15,' ')}"
            )
        print()
        print("*Full players rank rapport exported to data/exports/\n")

    def players_name_rapport(self) -> list:
        """export a players list rapport sorted by last-name (.xlsx) and print a preview of it"""

        players = self.tournament_players()
        data = [
            {
                "last_name": s[0],
                "first_name": s[1],
                "birthdate": s[2],
                "ine": s[3],
                "tournament": self.name,
                "status": self.status,
                "round": self.current_round,
            }
            for s in players
        ]

        data_to_export = pandas.DataFrame.from_records(data)
        file_path = (
            "./data/exports/tournament_(" + self.name + ")_players_name_rapport.xlsx"
        )
        data_to_export.to_excel(file_path)

        return players

    @classmethod
    def tournaments_rapport(self) -> list:
        """export tournaments data to an excel rapport and print a preview of it"""

        tournaments_data = []
        for t in self.table().all():
            tournament = [
                t["name"],
                t["place"],
                t["description"],
                t["status"],
                t["start_date"],
                t["end_date"],
                len(list(t["players_score"].keys())),
                t["number_of_rounds"],
                t["current_round"],
            ]
            tournaments_data.append(tournament)

        data = [
            {
                "name": p[0],
                "place": p[1],
                "description": p[2],
                "status": p[3],
                "start_date": p[4],
                "end_date": p[5],
                "number_of_players": p[6],
                "number_of_rounds": p[7],
                "current_round": p[8],
            }
            for p in tournaments_data
        ]

        data_to_export = pandas.DataFrame.from_records(data)
        file_path = "./data/exports/tournaments_rapport.xlsx"
        data_to_export.to_excel(file_path)

        return tournaments_data

    def tournament_rapport(self) -> list:
        """export tournament data to an excel rapport and print a preview of it"""

        data = [
            {
                "name": self.name,
                "place": self.place,
                "description": self.description,
                "status": self.status,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "number_of_players": len(list(self.players_score.keys())),
                "number_of_rounds": self.number_of_rounds,
                "current_round": self.current_round,
            }
        ]

        data_to_export = pandas.DataFrame.from_records(data)
        file_path = "./data/exports/tournament_(" + self.name + ")_rapport.xlsx"
        data_to_export.to_excel(file_path)

        return [
            self.name,
            self.place,
            self.status,
            self.start_date,
            self.end_date,
        ]

    def rounds_rapport(self) -> list:
        """export rounds data of tournament to an excel rapport and print a preview of it"""

        rounds_list = self.rounds_list
        rounds_rapport = []
        i = 1
        for r in rounds_list:
            round = Round.load(r)
            for match in round.match_list:
                rounds_rapport.append(
                    [
                        "match_" + str(i),
                        "white",
                        "⚪ " + Player.find_player(match[0][0])[0]["last_name"],
                        match[0][1],
                        match[1][1],
                        "⚫ " + Player.find_player(match[1][0])[0]["last_name"],
                        "black",
                        "round_" + str(round.number),
                        round.status,
                        match[0][0],
                        match[1][0],
                        self.name,
                        self.status,
                    ]
                )
                i += 1

        data = [
            {
                "match": p[0],
                "player1_color": p[1],
                "player1_name": p[2],
                "player1_score": p[3],
                "player2_score": p[4],
                "player2_name": p[5],
                "player2_color": p[6],
                "round_number": p[7],
                "round_status": p[8],
                "player1_ine": p[9],
                "player2_ine": p[10],
                "tournament_name": p[11],
                "tournament_status": p[12],
            }
            for p in rounds_rapport
        ]

        data_to_export = pandas.DataFrame.from_records(data)
        file_path = (
            "./data/exports/rounds_rapport_of_tournament_(" + self.name + ").xlsx"
        )
        data_to_export.to_excel(file_path)

        return rounds_rapport


""" reboot functions """


def boot_next_round():
    """next_rount"""
    tournament = Tournament.load("TOURNOI_1")

    tournament.next_round()

    tournament.update_match_score(0, 1, 0)
    tournament.update_match_score(1, 0.5, 0.5)
    tournament.update_match_score(2, 0, 1)

    tournament.update_players_score()


def reboot_tournament():
    """create a 2 fakes tournaments

    tournament_1 > complete
    tournament_2 > without player and without round
    """

    Round.table().truncate()
    Tournament.table().truncate()
    ine_liste = ["AB12345", "AB12346", "AB12347", "AB12348", "AB12349", "AB12350"]
    tournament1 = Tournament("TOURNOI_1", "online")
    tournament1.create()
    tournament1.add_players_list(ine_liste)

    tournament2 = Tournament("TOURNOI_2", "web")
    tournament2.create()

    # first round

    tournament1.first_round()

    tournament1.update_match_score(0, 1, 0)
    tournament1.update_match_score(1, 0.5, 0.5)
    tournament1.update_match_score(2, 0, 1)

    tournament1.update_players_score()

    # round 2 :

    boot_next_round()

    # round 3 :

    boot_next_round()

    # round 4 :

    boot_next_round()

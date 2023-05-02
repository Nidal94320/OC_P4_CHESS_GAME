""" class tournament """

import logging
from random import shuffle

from tinydb import TinyDB, where
import pandas

from models.players import Player
from models.rounds import Round, timestamp


class Tournament:
    def __init__(
        self,
        name: str,
        place: str,
        start_date=timestamp(),
        end_date="(not finished)",
        status="created",
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

    @classmethod
    def load(self, tournament_name: str):
        """load tournament instance from its name in json"""

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
        """update tournament data in json by its name"""

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
        """delete a tournament and its rounds in json"""

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
        """return tournament players list with all its attributes"""

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
        """add a players list to a tournament instance and database

        if player is in players table and not in tournaments table

        return the number of players added (used in view)"""

        if self.status == "created":
            added_players = 0
            players_score = {}
            for ine in players_ine:
                if ine in Player.players_ine():
                    if ine not in list(self.players_score.keys()):
                        players_score[ine] = 0
                        added_players += 1

            self.players_score = players_score

            return added_players
        else:
            logging.error(
                "It is impossible to add players in a running or finished tournament!"
            )

    def first_round(self):
        """generate a random round from shuffled players list

        used for the first round or if current_round >= number of players -1
        """

        if (self.status == "created" and len(self.players_score) >= 4) or (
            (self.current_round >= len(self.players_score) - 1)
            and (self.rounds_status())
            and (self.status == "running")
        ):
            round = Round(
                self.name,
                self.name + "_round_" + str(self.current_round + 1),
                self.current_round + 1,
            )
            players_ine_list = list(self.players_score.keys())
            round.first_round(players_ine_list)

            self.status = "running"
            self.current_round += 1
            rounds_list = self.rounds_list
            rounds_list.append(round.name)
            self.rounds_list = rounds_list

            round.create()
            self.update()

        elif len(self.players_score) < 4:
            logging.error(
                "A minimum of 4 players is required to start the tournament !"
            )

        elif not self.rounds_status():
            logging.error("The previous round isn't finished !")

        elif self.status != "created" and (
            self.current_round < len(self.players_score) - 1
        ):
            logging.error("Please use the 'next_round' class method !")

        elif self.status == "finished":
            logging.error("The tournament is finished !")

    def update_match_result(
        self,
        index_of_match: int,
        player1_score: float,
        player2_score: float,
        index_of_round=-1,
    ):
        """update match score of one round (update the last round if no present value)"""

        try:
            round = Round.load(self.rounds_list[index_of_round])
        except IndexError:
            logging.error("There is no round at this index in the tournament !")

        try:
            round.update_match_result(index_of_match, player1_score, player2_score)
            round._status()
            round.update()
            self._status()
        except UnboundLocalError:
            logging.error("There is no round at this index in the tournament !")

    def rounds_status(self) -> bool:
        """check if all created rounds of the tournament are finished

        return a boolean: True if all round are finished, False for the reverse"""

        return Round.rounds_status(self.rounds_list)

    def update_players_score(self):
        """update players_score and update database if all created rounds are finished"""

        if self.rounds_status():
            players_ine_list = list(self.players_score.keys())
            self.players_score = Round.update_players_score(
                players_ine_list, self.rounds_list
            )

            self.update()
        else:
            logging.error(
                "All created rounds must be finished to update the players score !"
            )

    def players_rank(self) -> list:
        """generate players ine list sorted by rank"""

        players_ine = []
        for p in sorted(list(self.players_score.items()), key=lambda p: (-p[1])):
            players_ine.append(p[0])

        return players_ine

    def next_round(self):
        """generate a next round from players list sorted by rank
        only if tournament status is 'running' and current_round < number of players -1
        """

        if (self.status == "running") and (
            (self.current_round < len(self.players_score) - 1)
            and (self.rounds_status())
        ):
            round = Round(
                self.name,
                self.name + "_round_" + str(self.current_round + 1),
                self.current_round + 1,
            )
            played_matchs = Round.played_matchs(self.rounds_list)
            round.next_round(self.players_rank(), played_matchs)
            self.current_round += 1
            rounds_list = self.rounds_list
            rounds_list.append(round.name)
            self.rounds_list = rounds_list

            round.create()
            self.update()

        elif not self.rounds_status():
            logging.error("The previous round isn't finished !")

        elif self.status == "finished":
            logging.error("The tournament is finished !")

        elif (self.status == "created") or (
            self.current_round >= len(self.players_score) - 1
        ):
            logging.error("Please use the 'first_round' class method !")

    def _status(self) -> bool:
        """Verify the current status of the tournament and update it if it has concluded

        return True if the tournament is finished"""

        if self.rounds_status() and self.current_round == self.number_of_rounds:
            self.status = "finished"
            self.end_date = timestamp()
            self.update()
            return True
        else:
            return False

    def draw_round(self):
        """call 'first_round' class method if tournament is 'created' or current_round >= number of players -1

        call 'next_round' class method if tournament is 'running' and current_round < number of players -1
        """

        if self.status != "finished":
            if self.status == "created" and len(self.players_score) >= 4:
                self.first_round()
                logging.info("'first_round' class method is used")

            if (self.current_round >= len(self.players_score) - 1) and (
                self.rounds_status()
            ):
                self.first_round()
                logging.info("'first_round' class method is used")

            if (self.status == "running") and (
                (self.current_round < len(self.players_score) - 1)
                and (self.rounds_status())
            ):
                self.next_round()
                logging.info("'next_round' class method is used")

        else:
            logging.error("The tournament is finished !")

    def full_player_ranking(self):
        """return the list of player ranking with its full attributes"""

        players_rank_rapport = []
        players = self.players_rank()

        i = 1
        for player in players:
            p = Player.find_player(player)
            s = [
                str(i),
                self.players_score[player],
                p[0]["last_name"],
                p[0]["first_name"],
                p[0]["ine"],
                self.name,
                self.status,
                self.current_round,
            ]
            players_rank_rapport.append(s)
            i += 1

        return players_rank_rapport

    def get_matchs_list(self) -> list:
        """return the matchs_list of the current round if there are still onging matchs"""

        last_round_name = self.rounds_list[-1]
        round = Round.load(last_round_name)
        if not round._status():
            matchs_list = round.get_matchs_list()
            return matchs_list
        else:
            return []

    """ rapport class methode """

    # reporter le print dans la vue
    def players_rank_rapport(self):
        """Export the tournament players ranking as a report (.xlsx) and return a list of it."""

        players_rank_rapport = []
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
            players_rank_rapport.append(s)
            i += 1

        data = [
            {
                "rank": row[0],
                "score": row[1],
                "last_name": row[2],
                "first_name": row[3],
                "ine": row[4],
                "tournament": self.name,
                "status": self.status,
                "round": self.current_round,
            }
            for row in players_rank_rapport
        ]
        data_to_export = pandas.DataFrame.from_records(data)
        file_path = (
            "./data/exports/tournament_(" + self.name + ")_players_rank_rapport.xlsx"
        )
        data_to_export.to_excel(file_path)

        # les prints doivent être reporté dans la vue du tournoi !

        print()
        print(" Rank       | Score      | Last-Name       | First-Name      | Ine")
        print(
            "____________|____________|_________________|_________________|____________"
        )
        for y in players_rank_rapport:
            print(
                f" {str(y[0]).ljust(10,' ')} | {str(y[1]).ljust(10,' ')} | {y[2].ljust(15,' ')} | {y[3].ljust(15,' ')} | {y[4].ljust(15,' ')}"
            )
        print()
        print("*Full players rank rapport exported to data/exports/\n")

    def players_name_rapport(self) -> list:
        """Export the tournament players list sorted by last-name as a report (.xlsx)
        and return a list of it."""

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
        """export tournaments data as a rapport (.xlsx) and return a list of it."""

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
        """export the tournament data as a rapport (.xlsx) and return a list of it."""

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
        """ "Export the tournament's rounds data as a report (.xlsx) and return a list of it."""

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

    """ class methode for demo """

    @classmethod
    def reboot(self):
        """create a 2 fakes tournaments"""

        Round.table().truncate()
        self.table().truncate()

        tournament1 = Tournament("TOURNOI_1", "ONLINE")
        ine_liste = ["AB12345", "AB12346", "AB12347", "AB12348"]
        self.add_players_list(tournament1, ine_liste)
        self.create(tournament1)

        tournament2 = Tournament("TOURNOI_2", "WEB")
        self.create(tournament2)


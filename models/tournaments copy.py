""" class tournament """

from datetime import datetime
from random import shuffle
from itertools import combinations

from tinydb import TinyDB, where
import pandas

from models.players import Player
from models.rounds import Round


def timestamp():
    # mettre que la date
    timestamp = [
        str(datetime.now())[0:10],
        str(datetime.now())[11:16].replace(":", "h"),
    ]

    return timestamp


class Tournament:
    """Class tournament"""

    def __init__(
        self,
        name: str,
        place: str,
        start_end=[timestamp(), ["...", "..."]],
        status="ongoing",
        description="",
        players_rank=[],
        number_of_rounds=4,
        current_round=0,
        round_status="",
        round_start_end=[],
        rounds_list=[],
        played_matchs=[],
    ):
        self.name = name
        self.place = place
        self.start_end = start_end
        self.status = status
        self.description = description
        self.players_rank = players_rank
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.round_status = round_status
        self.round_start_end = round_start_end
        self.rounds_list = rounds_list
        self.played_matchs = played_matchs

    def __str__(self):
        return f"{self.__dict__}"

    def __repr__(self):
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
    def load(self, tournament_name: str):
        """load instance from json"""

        if len(self.find(tournament_name)) > 0:
            tournament = self.find(tournament_name)

            return Tournament(
                tournament[0]["name"],
                tournament[0]["place"],
                tournament[0]["start_end"],
                tournament[0]["status"],
                tournament[0]["description"],
                tournament[0]["players_rank"],
                tournament[0]["number_of_rounds"],
                tournament[0]["current_round"],
                tournament[0]["round_status"],
                tournament[0]["round_start_end"],
                tournament[0]["rounds_list"],
                tournament[0]["played_matchs"],
            )
        else:
            return []

    @classmethod
    def find(self, tournament_name: str):
        """Look for a tournament in table by its name

        Take as argument a tournament_name(str)

        return found result"""

        return self.table().search(where("name") == tournament_name)

    def update(self):
        """update tournament data in json
        (only tournament_name can't be updated)"""

        self.table().update(
            {
                "place": self.place,
                "start_end": self.start_end,
                "status": self.status,
                "description": self.description,
                "players_rank": self.players_rank,
                "number_of_rounds": self.number_of_rounds,
                "current_round": self.current_round,
                "round_status": self.round_status,
                "round_start_end": self.round_start_end,
                "rounds_list": self.rounds_list,
                "played_matchs": self.played_matchs,
            },
            where("name") == self.name,
        )

    @classmethod
    def get_all(self, tournament_name: str) -> list:
        "get all data from tournament"

        return self.table().search(where("name") == tournament_name)[0]

    @classmethod
    def get_rounds_list(self, tournament_name: str) -> list:
        """get all rounds matchs from tournament"""

        return self.get_all(tournament_name)["rounds_list"]

    @classmethod
    def get_current_round(self, tournament_name: str) -> int:
        """get number of current round from tournament"""

        return self.get_all(tournament_name)["current_round"]

    @classmethod
    def get_round(self, tournament_name: str) -> list:
        """get all matchs of current round from tournament"""

        return self.get_all(tournament_name)["rounds_list"][
            self.get_current_round(tournament_name) - 1
        ]

    @classmethod
    def get_players(self, tournament_name: str) -> list:
        """get all players from tournament"""

        return self.get_all(tournament_name)["players_rank"]

    @classmethod
    def get_played_matchs(self, tournament_name: str) -> list:
        """get all played matchs from tournament"""

        return self.get_all(tournament_name)["played_matchs"]

    def add_player(self, player_ine: str):
        """add a player to tournament in instance and database"""

        found_player = Player.find_player(player_ine)
        self.players_rank.append([found_player[0]["ine"], 0])

    def add_players_list(self, players_ine: list):
        """add a players list to tournament from an ine list in instance and database"""

        for ine in players_ine:
            found_player = Player.find_player(ine)

            self.players_rank.append([found_player[0]["ine"], 0])

    @classmethod
    def players_name(self, tournament_name: str) -> list:
        """generate players list sorted by last_name from tournament"""

        sorted_list = []
        players = self.get_players(tournament_name)
        for player in players:
            p = Player.find_player(player[0])
            d = [
                p[0]["last_name"],
                p[0]["first_name"],
                p[0]["birthdate"],
                p[0]["ine"],
            ]
            sorted_list.append(d)

        return sorted(sorted_list, key=lambda p: (p[0]))

    @classmethod
    def players_ranking(self, tournament_name: str) -> list:
        """generate players_list sorted by score from tournament"""

        players = self.get_players(tournament_name)

        return sorted(players, key=lambda p: (-p[1]))

    def shuffle_players(self, tournament_name) -> list:
        """shuffle players list in instance and database"""

        players_rank = self.get_players(tournament_name)
        shuffle(players_rank)

        return players_rank

    @classmethod
    def random_round(self, tournament_name) -> list:
        """generate round from shuffled players list"""

        participants = self.get_players(tournament_name)
        shuffle(participants)
        number_of_matchs = len(participants) // 2
        round = []
        played_matchs = self.get_played_matchs(tournament_name)

        for i in range(number_of_matchs):
            match = ([participants[i][0], ""], [participants[i + 1][0], ""])
            round.append(match)

            duel = [participants[i][0], participants[i + 1][0]]

            reverse_duel = [participants[i + 1][0], participants[i][0]]
            played_matchs.append(duel)
            played_matchs.append(reverse_duel)
            """supprimer le premier élément de la liste >
            i skip le nouveau premier élément au prochain tour >
            comme ceci le premier couple de joueur de la liste n'apparait plus dans duel """
            participants.pop(0)

        return round, played_matchs

    def update_instance(self, round: list, played_matchs: list):
        """update round data in instance"""

        self.current_round += 1
        self.round_status = "ongoing"
        self.rounds_list.append(round)
        self.round_start_end.append([timestamp(), ""])
        self.played_matchs = played_matchs

    @classmethod
    def update_json(self, tournament):
        """Update round data in json"""

        self.table().update(
            {
                "rounds_list": tournament.rounds_list,
                "played_matchs": tournament.played_matchs,
                "current_round": tournament.current_round,
                "round_start_end": tournament.round_start_end,
                "round_status": tournament.round_status,
            },
            where("name") == tournament.name,
        )

    def first_round2(self):
        """generate first round and save it in instance and database"""

        if self.current_round == 0:
            round, played_matchs = self.random_round(self.name)

            self.update_instance(round, played_matchs)
            self.update()

    @classmethod
    def first_round(self, tournament):
        """generate first round and save it in instance and database"""

        if self.current_round == 0:
            round, played_matchs = self.random_round(tournament)

            self.update_instance(tournament, round, played_matchs)
            self.update_json(tournament)

    @classmethod
    def update_match(self, tournament, match_indice: int, score: list):
        """update the score of one match in current round"""

        rounds = self.get_all(tournament)["rounds_list"]

        # modifie le score du joueur 1 dans la match
        rounds[self.get_current_round(tournament) - 1][match_indice][0][1] = score[0]

        # modifie le score du joueur 2
        rounds[self.get_current_round(tournament) - 1][match_indice][1][1] = score[1]

        # met à jour l'attribut d'instance tournament.rounds_list
        tournament.rounds_list = rounds

        # met à jour "rounds_list" dans json
        self.table().update(
            {"rounds_list": tournament.rounds_list},
            where("name") == tournament.name,
        )

    @classmethod
    def update_round_status(self, tournament) -> bool:
        """test if all matchs are finished and update the current round status to "finished" """

        # recuperation du round en cours
        round = self.get_round(tournament)
        # constante ) placer en haut
        score = ["0", "0.5", "1", 0, 0.5, 1]
        # vérification si chaque match contient bien un score
        for match in round:
            if (match[0][1] in score) and (match[1][1] in score):
                status = True
            else:
                status = False
            if status == False:
                break
        # MAJ du statut du round
        if status:
            tournament.round_status = "finished"
            # vérifie si le tournoi est terminé
            if (
                self.get_current_round(tournament)
                == self.get_all(tournament)["number_of_rounds"]
            ):
                tournament.status = "finished"
                start_end = self.get_all(tournament)["start_end"]
                start_end[1] = timestamp()
                tournament.start_end = start_end
                self.table().update(
                    {
                        "status": tournament.status,
                        "start_end": tournament.start_end,
                    },
                    where("name") == tournament.name,
                )
            # MAJ horodatage fin round
            round_start_end = self.get_all(tournament)["round_start_end"]
            round_start_end[self.get_current_round(tournament) - 1][1] = timestamp()
            tournament.round_start_end = round_start_end

            self.table().update(
                {
                    "round_status": tournament.round_status,
                    "round_start_end": tournament.round_start_end,
                },
                where("name") == tournament.name,
            )

        return status

    @classmethod
    def update_players_rank(self, tournament):
        """update players rank when a round is finished"""

        # test if all matchs are finished
        if self.update_round_status(tournament):
            players = self.get_players(tournament)
            rounds = self.get_rounds_list(tournament)
            updated_players = []

            for player in players:
                player_ine = player[0]
                player_score = 0
                for round in rounds:
                    for match in round:
                        if match[0][0] == player_ine:
                            player_score += match[0][1]
                        if match[1][0] == player_ine:
                            player_score += match[1][1]
                updated_players.append([player_ine, player_score])

        tournament.players_rank = updated_players
        self.table().update(
            {"players_rank": updated_players},
            where("name") == tournament.name,
        )

    @classmethod
    def unplayed_matchs(self, tournament):
        """generate unplayed_matchs list sorted by players rank"""
        # au 4ème tour j'ai parfois un doublon de match (déjà présent dans un des tours précédents)

        # génère une liste de duel non joué
        participants = self.players_rank(tournament)
        unplayed_matchs = []
        played_matchs = self.get_played_matchs(tournament)

        i = 1
        presence = False

        for player1 in participants[:-1]:
            for player2 in participants[i:]:
                duel = [player1[0], player2[0]]
                if duel not in played_matchs:
                    for game in unplayed_matchs:
                        if duel[0] in game or duel[1] in game:
                            presence = True
                    if presence == False:
                        unplayed_matchs.append(duel)
                    presence = False

            i = i + 1

        return unplayed_matchs

    @classmethod
    def unplayed_matchs_2(self, tournament):
        """generate unplayed_matchs list sorted by rank"""
        # au 4ème tour j'ai parfois un doublon de match (déjà présent dans un des tours précédents)

        played_matchs = Tournament.get_played_matchs(tournament)
        partipants = []
        for player in self.players_ranking(tournament):
            partipants.append(player[0])

        unplayed_matchs = []
        partcipants_in_unplayed_matchs = []

        # on vérfie si un des joueurs de la combi
        # n'est pas déjà dans unplayed_matchs avant de l'ajouter à celui-ci """

        for duel in combinations(partipants, 2):
            if (
                (duel[0] not in partcipants_in_unplayed_matchs)
                and (duel[1] not in partcipants_in_unplayed_matchs)
                and ([str(duel[0]), str(duel[1])] not in played_matchs)
            ):
                unplayed_matchs.append([str(duel[0]), str(duel[1])])
                partcipants_in_unplayed_matchs.append(duel[0])
                partcipants_in_unplayed_matchs.append(duel[1])

        return unplayed_matchs

    @classmethod
    def next_round(self, tournament):
        """generate round from unplayed_matchs when it's possible or from random_round

        return the method "from unplayed_matchs" or "from random_round"
        """
        # au 4ème tour j'ai parfois un doublon de match (ayant déjà dans un des tours précédents)

        current_round = int(self.get_current_round(tournament))
        number_of_rouds = int(self.get_all(tournament)["number_of_rounds"])
        condition_1 = current_round < number_of_rouds
        condition_2 = self.update_round_status(tournament)

        if condition_1 and condition_2:
            participants = self.players_ranking(tournament)
            number_of_matchs = len(participants) // 2
            round = []
            played_matchs = self.get_played_matchs(tournament)
            unplayed_matchs = self.unplayed_matchs_2(tournament)

            # génére le round à partir de unplayed_matchs si unplayed_duel
            # contient un nombre suffisant
            if len(unplayed_matchs) == number_of_matchs:
                for duel in unplayed_matchs:
                    match = ([duel[0], ""], [duel[1], ""])
                    round.append(match)

                    duel = [match[0][0], match[1][0]]
                    reverse_duel = [match[1][0], match[0][0]]
                    played_matchs.append(duel)
                    played_matchs.append(reverse_duel)
            else:
                round, played_matchs = self.random_round(tournament)

            self.update_instance(tournament, round, played_matchs)
            self.update_json(tournament)

    # rapport methode

    @classmethod
    def players_name_rapport(self, tournament_name):
        """export players_name to an excel rapport and read it"""

        players = self.players_name(tournament_name)
        data = [
            {
                "last_name": p[0],
                "first_name": p[1],
                "birthdate": p[2],
                "ine": p[3],
                "tournament_name": tournament_name,
            }
            for p in players
        ]

        data_to_export = pandas.DataFrame.from_records(data)
        file_path = (
            "./data/tournaments/tournament_("
            + tournament_name
            + ")_registered_players_rapport.xlsx"
        )
        data_to_export.to_excel(file_path)
        data_saved = pandas.read_excel(file_path, usecols="B:F")
        print()
        print(data_saved)
        print()

    @classmethod
    def tournaments_rapport(self):
        """export tournaments data to an excel rapport and read it"""

        tournaments_data = []
        for t in self.table().all():
            tournament = [
                t["name"],
                t["place"],
                t["description"],
                t["status"],
                t["start_end"][0],
                t["start_end"][1],
                len(t["players_rank"]),
                t["number_of_rounds"],
                t["current_round"],
                t["round_status"],
            ]
            tournaments_data.append(tournament)

        data = [
            {
                "name": p[0],
                "place": p[1],
                "description": p[2],
                "status": p[3],
                "start_date": p[4][0],
                "start_hour": p[4][1],
                "end_date": p[5][0],
                "end_hour": p[5][1],
                "number_of_player": p[6],
                "number_of_rounds": p[7],
                "current_round": p[8],
                "round_status": p[9],
            }
            for p in tournaments_data
        ]

        data_to_export = pandas.DataFrame.from_records(data)
        file_path = "./data/tournaments/tournaments_rapport.xlsx"
        data_to_export.to_excel(file_path)
        data_saved = pandas.read_excel(file_path, usecols="B,C,E,J,K,L")
        print()
        print(data_saved)
        print()

    @classmethod
    def tournament_rapport(self, name):
        """export tournaments data to an excel rapport and read it"""

        tournaments_data = []
        for t in self.table().all():
            tournament = [
                t["name"],
                t["place"],
                t["description"],
                t["status"],
                t["start_end"][0],
                t["start_end"][1],
                len(t["players_rank"]),
                t["number_of_rounds"],
                t["current_round"],
                t["round_status"],
            ]
            tournaments_data.append(tournament)

        data = [
            {
                "name": p[0],
                "place": p[1],
                "description": p[2],
                "status": p[3],
                "start_date": p[4][0],
                "start_hour": p[4][1],
                "end_date": p[5][0],
                "end_hour": p[5][1],
                "number_of_player": p[6],
                "number_of_rounds": p[7],
                "current_round": p[8],
                "round_status": p[9],
            }
            for p in tournaments_data
        ]

        data_to_export = pandas.DataFrame.from_records(data)
        file_path = "./data/tournaments/tournaments_rapport.xlsx"
        data_to_export.to_excel(file_path)
        data_saved = pandas.read_excel(file_path, usecols="B,C,E,F,G,H,I")
        print()
        print(data_saved[data_saved.name == name])
        print()

    @classmethod
    def players_rank_rapport(self, tournament_name: str):
        """export players_rank to an excel rapport and read it"""

        players_rank = []
        players = self.players_ranking(tournament_name)
        i = 1
        for player in players:
            p = Player.find_player(player[0])
            s = [
                i,
                p[0]["last_name"],
                p[0]["first_name"],
                p[0]["ine"],
                player[1],
                self.get_current_round(tournament_name),
            ]
            players_rank.append(s)
            i += 1

        data = [
            {
                "rank": r[0],
                "last_name": r[1],
                "first_name": r[2],
                "ine": r[3],
                "score": r[4],
                "current_round": r[5],
                "tournament_name": self.get_all(tournament_name)["name"],
            }
            for r in players_rank
        ]
        data_to_export = pandas.DataFrame.from_records(data)
        file_path = (
            "./data/tournaments/tournament_("
            + tournament_name
            + ")_players_rank_rapport.xlsx"
        )
        data_to_export.to_excel(file_path)
        data_saved = pandas.read_excel(file_path, usecols="B:H")
        print()
        print(data_saved)
        print()

    @classmethod
    def tournament_rounds_rapport(self, name):
        pass

""" class Player """

from tinydb import TinyDB, where
import pandas


class Player:
    """Create, edit Player in database(JSON) or read database


    To instantiate a player :
    - last_name(str)
    - first_name(str)
    - birthdate(str)
    - ine (str)"""

    def __init__(self, last_name: str, first_name: str, birthdate: str, ine: str):
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.ine = ine

    def __str__(self):
        """used in print"""

        return f"{self.__dict__}"

    def __repr__(self):
        return str(self)

    @classmethod
    def db(self):
        """Create a JSON file as database"""

        return TinyDB("./data/players/players.json")

    @classmethod
    def table(self):
        """Create 'Players' table in database"""

        return self.db().table("Players")

    def create(self):
        """Create player in database"""

        self.table().insert(self.__dict__)

    @classmethod
    def load(self, ine):
        """load instance from json"""

        if len(self.find_player(ine)) > 0:
            player = self.find_player(ine)

            return Player(
                player[0]["last_name"],
                player[0]["first_name"],
                player[0]["birthdate"],
                player[0]["ine"],
            )
        else:
            return []

    def update(self):
        """update players data in json"""
        self.table().update(
            {
                "last_name": self.last_name,
                "first_name": self.first_name,
                "birthdate": self.birthdate,
            },
            where("ine") == self.ine,
        )

    def delete(self):
        """delete a player from Players table(json)"""

        self.table().remove(where("ine") == self.ine)

    @classmethod
    def read_all(self):
        """Display players table sorted by last_name"""

        def cle(players):
            return players["last_name"]

        return sorted(self.table().all(), key=cle)

    @classmethod
    def find_player(self, ine):
        """Look for a player in players table by ine

        Take as argument an ine(str): chess player national id

        return found result"""

        return self.table().search(where("ine") == ine)

    @classmethod
    def delete_table(self):
        """Delete all data from players table"""

        self.table().truncate()

    @classmethod
    def boot(self):
        """create fake players in database for demo"""

        player1 = Player(
            last_name="ZIDANE",
            first_name="Zinedine",
            birthdate="23/06/1972",
            ine="AB12345",
        )
        self.create(player1)

        player2 = Player(
            last_name="MARADONA",
            first_name="Diego",
            birthdate="30/10/1960",
            ine="AB12346",
        )
        self.create(player2)

        player3 = Player(
            last_name="RONALDO",
            first_name="Christiano",
            birthdate="05/02/1985",
            ine="AB12347",
        )
        self.create(player3)

        player4 = Player(
            last_name="MESSI",
            first_name="Lionel",
            birthdate="24/06/1987",
            ine="AB12348",
        )
        self.create(player4)

        player5 = Player(
            last_name="INIESTA",
            first_name="Andres",
            birthdate="24/06/1987",
            ine="AB12349",
        )
        self.create(player5)

        player6 = Player(
            last_name="VAN-BASTEN",
            first_name="Marco",
            birthdate="24/06/1987",
            ine="AB12350",
        )
        self.create(player6)

    @classmethod
    def reboot(self):
        """Clear players table and create fake players in it for demo"""
        self.delete_table()
        self.boot()

    @classmethod
    def rapport(self):
        """export system's players to an excel rapport and read it"""

        players_rapport = []

        for player in self.read_all():
            players_rapport.append(
                [
                    player["last_name"],
                    player["first_name"],
                    player["birthdate"],
                    player["ine"],
                ]
            )
        file_path = "./data/exports/system_players_rapport.xlsx"

        data = [
            {
                "last_name": p[0],
                "first_name": p[1],
                "birthdate": p[2],
                "ine": p[3],
            }
            for p in players_rapport
        ]

        data_to_export = pandas.DataFrame.from_records(data)
        data_to_export.to_excel(file_path)

        return players_rapport

""" class Round """

from datetime import datetime

from tinydb import TinyDB, where


def timestamp():
    timestamp = str(datetime.now())[0:10]

    return timestamp


class Round:
    """Class Round"""

    def __init__(
        self,
        tournament_name: str,
        name: str,
        number: int,
        start_date=timestamp(),
        end_date="",
        status="ongoing",
        match_list=[],
    ):
        self.tournament_name = tournament_name
        self.name = name
        self.number = number
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.match_list = match_list

    def __str__(self):
        """used in print"""

        return f"{self.__dict__}"

    def __repr__(self):
        """used in print"""

        return str(self)

    @classmethod
    def db(self):
        """Create a JSON file as database"""

        return TinyDB("./data/rounds/rounds.json")

    @classmethod
    def table(self):
        """Create 'Rounds' table in database"""

        return self.db().table("Rounds")

    def create(self):
        """Create a new round in Rounds table"""

        self.table().insert(self.__dict__)

    @classmethod
    def find(self, round_name: str) -> list:
        """Look for a round in table by its name

        Take as argument a round_name(str)

        return found result"""

        return self.table().search(where("name") == round_name)[0]

    @classmethod
    def load(self, round_name: str):
        """load instance from json"""

        if len(self.find(round_name)) == 7:
            round = self.find(round_name)

            return Round(
                round["tournament_name"],
                round["name"],
                round["number"],
                round["start_date"],
                round["end_date"],
                round["status"],
                round["match_list"],
            )
        else:
            return []

    def update(self):
        """update round data in json
        (only round.name can't be updated)"""

        self.table().update(
            {
                "tournament_name": self.tournament_name,
                "number": self.number,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "status": self.status,
                "match_list": self.match_list,
            },
            where("name") == self.name,
        )

    def delete(self):
        """delete a round from Rounds table(json)"""

        self.table().remove(where("name") == self.name)

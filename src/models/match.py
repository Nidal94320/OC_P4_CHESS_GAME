""" class Matchs """

from .player import Players


class Matchs:
    def __init__(
        self,
        index: int,
        match: tuple,
    ):
        self.index = index
        self.match = match

    def __str__(self):
        """Used in print."""

        p1_name = Players.find(self.match[0][0])[0]["last_name"]
        p1_score = self.match[0][1]
        p2_name = Players.find(self.match[1][0])[0]["last_name"]
        p2_score = self.match[1][1]

        return f"""\n                     Match {self.index}
            ⚪ {p1_name} {p1_score} - {p2_score} {p2_name} ⚫\n"""

    def __repr__(self):
        """Used in print."""
        return str(self)

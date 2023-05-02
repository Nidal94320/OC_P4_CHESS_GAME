""" class Match """
from .players import Player


class Match:
    def __init__(
        self,
        index: int,
        match: tuple,
    ):
        self.index = index
        self.match = match

    def __str__(self):
        """Used in print."""

        return f"""\n                  Match {self.index}
        ⚪ {Player.find_player(self.match[0][0])[0]["last_name"]} {self.match[0][1]} - {self.match[1][1]} {Player.find_player(self.match[1][0])[0]["last_name"]} ⚫\n"""

    def __repr__(self):
        """Used in print."""
        return str(self)


# match = Match(0, (["player1", ""], ["player2", ""]))
# print(match)
"""     if self.match[0][1] == "":
            player1_score = 0
        else:
            player1_score = self.match[0][1]

        if self.match[1][1] == "":
            player2_score = 0
        else:
            player2_score = self.match[1][1] """

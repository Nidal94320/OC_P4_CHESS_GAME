from datetime import datetime
from random import shuffle
from random import shuffle
from itertools import combinations

from tinydb import TinyDB, where
import pandas
from pprint import pprint

from models.tournaments import timestamp, Tournament
from models.rounds import Round
from models.players import Player
from models.matchs import Match


Tournament.reboot()

""" Round.table().truncate()
Tournament.table().truncate()

tournament1 = Tournament("TOURNOI_1", "online")
ine_liste = ["AB12345", "AB12346", "AB12347", "AB12348"]
tournament1.add_players_list(ine_liste)
tournament1.create()

tournament1.first_round()

tournament1.update_match_result(0, 1, 0)
tournament1.update_match_result(1, 0.5, 0.5)

tournament1.update_players_score()

# tournament1 = Tournament.load("TOURNOI_1")
tournament1.next_round()
tournament1.update_match_result(0, 1, 0)
tournament1.update_match_result(1, 0.5, 0.5) """

# tournament2 = Tournament("TOURNOI_2", "web")
# tournament2.create()

""" tournament4 = Tournament("TOURNOI_5", "web")
ine_liste = ["AB12345", "AB12346", "AB12347", "AB12348"]
tournament4.add_players_list(ine_liste)
tournament4.create()

tournament4.next_round()

tournament4.update_match_result(0, 1, 0)
tournament4.update_match_result(1, 0.5, 0.5)

tournament4.update_players_score() """
# tournament = Tournament.load("TOURNOI_1")
# print(len(tournament.get_matchs_list()))
SCORE = [0, 0.5, 1]
a="0"
b="0.5"
c=1
print(float(a))

# print(a.replace(".","").isdigit())


""" match_list = tournament.ongoing_matchs()
i = 1
for m in match_list:
    print(Match(i, m))
    i += 1 """
# name1 = Player.find_player(m[0][0])[0]["last_name"]
# print(name1)
# name2 = Player.find_player(m[1][0])[0]["last_name"]
# print(name2)
""" t = [
    tournament.name,
    tournament.status,
    str(tournament.current_round) + "/" + str(tournament.number_of_rounds),
]


print()
print(" __________________________________________________________________")
print("| Tournament name                | Status         | Current round  |")
print("|________________________________|________________|________________|")
print("|                                |                |                |")

print(f"| {t[0].ljust(30,' ')} | {t[1].ljust(14,' ')} | {t[2].ljust(14,' ')} |")
print("|________________________________|________________|________________|\n")

players = tournament.full_player_ranking()
# print(" Ranking   Name       Score ")
for p in players:
    print(f" {str(p[0])}  {p[2].ljust(10,' ')} {p[1]} pt") """

from datetime import datetime
from random import shuffle
from itertools import combinations

from tinydb import TinyDB, where
import pandas

from models.tournaments import timestamp, Tournament, reboot_tournament
from models.rounds import Round
from models.players import Player

reboot_tournament()

# tournament2 = Tournament("tournoi_2", "web")
# tournament2.create()
# print(len(Player.table().all()))
# print(Player.find_player("AB12349")[0]["last_name"])
"""
ine_liste_2 = ["AB12350", "AB12346", "AB12347", "AB12348", "AB12349", "AB12345"]
tournament2.add_players_list(ine_liste_2) """

""" Round.table().truncate()
Tournament.table().truncate()

tournament1 = Tournament("tournoi_1", "online")
ine_liste = ["AB12345", "AB12346", "AB12347", "AB12348", "AB12349", "AB12350"]
tournament1.create()
tournament1.add_players_list(ine_liste)

# first round


tournament1.first_round()


tournament1.update_match_score(0, 1, 0)
tournament1.update_match_score(1, 0.5, 0.5)
tournament1.update_match_score(2, 0, 1)


tournament1.update_players_score() """

# next round


""" tournament2 = Tournament.load("tournoi_1")
tournament2.next_round_1()

tournament2.update_match_score(0, 1, 0)
tournament2.update_match_score(1, 0.5, 0.5)
tournament2.update_match_score(2, 0, 1)


tournament2.update_players_score() """


# test
""" Round.table().truncate()
Tournament.table().truncate()

tournament1 = Tournament("tournoi_1", "online")
ine_liste = ["AB12345", "AB12346", "AB12347", "AB12348", "AB12349", "AB12350"]
tournament1.create()
tournament1.add_players_list(ine_liste)


# players = tournament1.players_rank()

# for p in combinations(players, 2):
#     print(p)

 """
""" tournament1.update_match_score(0, 0, 1)
tournament1.update_match_score(1, 0.5, 0.5)
tournament1.update_match_score(2, 1, 0)


tournament1.update_players_score() """


""" # test rapport (à lancer un par) :

tournament1.players_rank_rapport()
tournament1.players_name_rapport()
Tournament.tournaments_rapport()
tournament1.tournament_rapport()
tournament1.rounds_rapport() """

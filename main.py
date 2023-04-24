""" main : run chess game """

from models.players import Player
from models.tournaments import reboot_tournament
from controllers.main_controller import Controller

""" add 6 fake players for the demo """

Player.reboot()

""" create 2 fakes tournaments """
# besoin d'aide sur la méthode next_round
# de la class tournament

reboot_tournament()

if __name__ == "__main__":
    while True:
        controller = Controller()
        controller.run()

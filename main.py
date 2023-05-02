""" main : run chess game """

from models.players import Player
from models.tournaments import Tournament
from controllers.main_controller import Controller

""" add 6 fake players for the demo """

Player.reboot()

""" create 2 fakes tournaments for the demo"""

Tournament.reboot()


def main():
    while True:
        controller = Controller()
        controller.run()


if __name__ == "__main__":
    main()

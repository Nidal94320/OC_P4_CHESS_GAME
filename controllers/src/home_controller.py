"""Home Menu controller"""


from views.view_home_menu import ViewHomeMenu


class HomeController:
    """Home Menu controller"""

    def __init__(self):
        self.view_home = ViewHomeMenu()

    def home_menu(self):
        """home menu"""

        choice = self.view_home.home_menu()
        return choice

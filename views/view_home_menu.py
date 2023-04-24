"""Main menu view."""


class ViewHomeMenu:
    """Main menu view."""

    def home_menu(self):
        """display main menu"""
        print()
        print("-" * 80)
        print(
            """                          ♟️   Chess Game ♟️ 

                          Home Menu

            1 -- Player
            2 -- Tournament
            3 -- Rapport
            4 -- Exit"""
        )
        print("-" * 80)
        print()
        response = input("your choice > ")
        return response

""" Class tournament menu view"""


class ViewTournament:
    """tournament view."""

    def tournament_menu(self):
        """display tournament menu"""

        print("-" * 80)
        print(
            f"""                          ♟️   Chess Game ♟️ 

                          Tournament Menu
            
                          
            1 -- Create
            2 -- Play
            3 -- Edit
            4 -- Delete
            5 -- Back to Home Menu
            
            """
        )
        print("-" * 80)
        print()
        response = input("your choice > ")

        return response

    def invalid_choice(self):
        """used when invalid choice is selected"""

        print(f"\nInvalide choice !\n ")

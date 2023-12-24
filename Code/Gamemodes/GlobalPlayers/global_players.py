class GlobalPlayer:
    """Class that instanciates a GlobalPlayer object containing the information that is stored in the global player's sheet."""

    def __init__(self, player_name: str, list_name: str, list_from: str, list_sections: str, comment: str) -> None:
        """
        Constructor of the GlobalPlayer class.\n
        Parameters:
        -----------
        - `player_name`: `str`
            The global player's AMQ name.
        - `list_name`: `str`
            The name of the list (username from Anilist / MyAnimeList) where the shows are stored.
        - `list_from`: `str`
            Where the list is from (Anilist / MyAnimeList).
        - `list_sections`: `str`
            The sections from the list that must be used during the AMQ game that contains the shows from the global player.
        - `comment`: `str`
            A comment that the player has left as additional information.
        """
        self.player_name = player_name
        self.list_name = list_name
        self.list_from = list_from
        self.list_sections = list_sections
        self.comment = comment

    def __str__(self) -> str:
        """Return a string representation of the GlobalPlayer object. Use it to display global player info in a compressed way (e.g. displaying info from all global players)"""
        return f'{self.player_name} - {self.list_name}'

    def __repr__(self) -> str:
        """Return a string representation of the GlobalPlayer object. Use it to display global player info in a extended way (e.g. displaying info from only one global player)"""
        global_player = f'**Player selected:** {self.player_name}\n'
        global_player += f'**List name:** {self.list_name}\n'
        global_player += f'**From:** {self.list_from}\n'
        global_player += f'**Sections:** {self.list_sections}\n'
        global_player += f'**Comment:** {self.comment}'
        return global_player
class OG_Artist:
    """
    Class that instanciates an OG Artist object containing the information that is stored in the sheet.\n
    These are Anilist/MyAnimeList lists that have all the shows where the artist(s) sings in (songs from those shows by different artist can play).
    """

    def __init__(self, artist_name: str, list_name: str, score_range: str, list_sections: str, list_from: str, author_name: str) -> None:
        """
        Constructor of the OG_Artist class.\n
        Parameters:
        -----------
        - `artist_name`: `str`
            The name of the artist(s).
        - `list_name`: `str`
            The name of the list (username from Anilist / MyAnimeList) where the shows are stored.
        - `score_range`: `str`
            A string consisting of the Scores that the show(s) which contains songs from the artist(s), stored in the list, have (that must be set in the AMQ room settings).
        - `list_sections`: `str`
            The sections from the list that must be used during the AMQ game that contains the shows from the artist(s).
        - `list_from`: `str`
            Where the list is from (Anilist / MyAnimeList).
        - `author_name`: `str`
            The player who created the list.
        """
        self.artist_name = artist_name
        self.author_name = author_name
        self.list_name = list_name
        self.list_from = list_from
        self.list_sections = list_sections
        self.score_range = score_range

    def __str__(self) -> str:
        """Return a string representation of the OG Artist object. Use it to display artist info in a compressed way (e.g. displaying info from all artists)"""
        return f'**{self.artist_name}** // {self.list_name} // Score {self.score_range} // {self.list_sections} // {self.list_from}'

    def __repr__(self) -> str:
        """Return a string representation of the OG Artist object. Use it to display artist info in a extended way (e.g. displaying info from only one artist)"""
        artist = f'**Artist:** {self.artist_name}\n'
        artist += f'**List:** {self.list_name}\n'
        artist += f'**Score:** {self.score_range}\n'
        artist += f'**Sections:** {self.list_sections}\n'
        artist += f'**From:** {self.list_from}\n'
        artist += f'**Author:** {self.author_name}'
        return artist
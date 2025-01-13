class CQ_SpecialList:
    """
    Class that instanciates a CQ Special List object containing the information that is stored in the sheet.\n
    These are Community Quizes to get only the songs from the composer/shows/whatever rather than all songs from the shows like in OG_SpecialLists.
    """

    def __init__(self, community_quiz_id: str, special_list_name: str, community_quiz_name: str, number_of_songs: str, author_name: str) -> None:
        """
        Constructor of the CQ_Artist class.\n
        Parameters:
        -----------
        - `community_quiz_id`: `str`
            The ID of the Community Quiz.
        - `special_list_name`: `str`
            The name of the special list(s).
        - `community_quiz_name`: `str`
            The Community Quiz name.
        - `number_of_songs`: `str`
            The number of songs that the quiz has.
        - `author_name`: `str`
            The player who created the list.
        """
        self.community_quiz_id = community_quiz_id
        self.special_list_name = special_list_name
        self.community_quiz_name = community_quiz_name
        self.number_of_songs = number_of_songs
        self.author_name = author_name

    def __str__(self) -> str:
        """Return a string representation of the CQ Special List object. Use it to display special list info in a compressed way (e.g. displaying info from all special lists)"""
        return f'**{self.special_list_name}** // {self.community_quiz_id}: {self.community_quiz_name} // Score {self.number_of_songs} // {self.author_name}'

    def __repr__(self) -> str:
        """Return a string representation of the CQ Special List object. Use it to display special list info in a extended way (e.g. displaying info from only one special list)"""
        artist = f'**Special List:** {self.special_list_name}\n'
        artist += f'**Community Quiz:** {self.community_quiz_id}: {self.community_quiz_name}\n'
        artist += f'**Number of songs:** {self.number_of_songs}\n'
        artist += f'**Author:** {self.author_name}'
        return artist
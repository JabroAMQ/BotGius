class CQ_Artist:
    """
    Class that instanciates a CQ Artist object containing the information that is stored in the sheet.\n
    These are Community Quizes to get only the songs from the artist rather than all songs from the shows were the artist sings in.
    """

    def __init__(self, community_quiz_id: str, artist_name: str, community_quiz_name: str, number_of_songs: str, author_name: str) -> None:
        """
        Constructor of the CQ_Artist class.\n
        Parameters:
        -----------
        - `community_quiz_id`: `str`
            The ID of the Community Quiz.
        - `artist_name`: `str`
            The name of the artist(s).
        - `community_quiz_name`: `str`
            The Community Quiz name.
        - `number_of_songs`: `str`
            The number of songs that the quiz has.
        - `author_name`: `str`
            The player who created the list.
        """
        self.community_quiz_id = community_quiz_id
        self.artist_name = artist_name
        self.community_quiz_name = community_quiz_name
        self.number_of_songs = number_of_songs
        self.author_name = author_name

    def __str__(self) -> str:
        """Return a string representation of the CQ Artist object. Use it to display artist info in a compressed way (e.g. displaying info from all artists)"""
        return f'**{self.artist_name}** // {self.community_quiz_id}: {self.community_quiz_name} // Songs: {self.number_of_songs} // {self.author_name}'

    def __repr__(self) -> str:
        """Return a string representation of the CQ Artist object. Use it to display artist info in a extended way (e.g. displaying info from only one artist)"""
        artist = f'**Artist:** {self.artist_name}\n'
        artist += f'**Community Quiz:** {self.community_quiz_id} {self.community_quiz_name}\n'
        artist += f'**Number of songs:** {self.number_of_songs}\n'
        artist += f'**Author:** {self.author_name}'
        return artist
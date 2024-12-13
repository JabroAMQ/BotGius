class OG_SpecialList:
    """Class that instanciates a OG SpecialList object containing the information that is stored in the sheet."""

    def __init__(self, special_list_name: str, list_name: str, list_from: str, list_sections: str, difficulty_range: str, special_list_description: str, author_name: str) -> None:
        """
        Constructor of the OG Special List class.\n
        Parameters:
        -----------
        - `special_list_name`: `str`
            The name of the special list.
        - `list_name: `str`
            The name of the list (username from Anilist / MyAnimeList) where the shows are stored.
        - `list_from: `str`
            Where the list is from (Anilist / MyAnimeList).
        - `list_sections: `str`
            The sections from the list that must be used during the AMQ game that contains the shows from the special list.
        - `difficulty_range: `str`
            The difficulty range that has to be set in the AMQ game settings.
        - `special_list_description: `str`
            The description of the special list.
        - `author_name: `str`
            The player who created the list.
        """
        self.special_list_name = special_list_name
        self.special_list_description = special_list_description
        self.author_name = author_name
        self.list_name = list_name
        self.list_from = list_from
        self.list_sections = list_sections
        self.difficulty_range = difficulty_range

    def __str__(self) -> str:
        """Return a string representation of the OG SpecialList object. Use it to display special list info in a compressed way (e.g. displaying info from all special lists)"""
        special_list = f'**{self.special_list_name}**: {self.list_name} (From {self.list_from} // Sections: {self.list_sections} // Difficulty: {self.difficulty_range}'
        special_list += f' // Author: {self.author_name})\n{self.special_list_description}'
        return special_list

    def __repr__(self) -> str:
        """Return a string representation of the OG SpecialList object. Use it to display special list info in a extended way (e.g. displaying info from only one special list)"""
        special_list = f'**Special List:** {self.special_list_name}\n'
        special_list += f'**List Name:** {self.list_name}\n'
        special_list += f'**From:** {self.list_from}\n'
        special_list += f'**Sections:** {self.list_sections}\n'
        special_list += f'**Difficulty Range:** {self.difficulty_range}\n'
        special_list += f'**Description:** {self.special_list_description}\n'
        special_list += f'**Author:** {self.author_name}\n'
        return special_list
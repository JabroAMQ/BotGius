class Male_Artist:
    """Class that instanciates a Male Artist object containing the information that is stored in the spotlight's sheet."""
    def __init__(self, artist_name: str, community_quiz_id: str) -> None:
        """
        Constructor of the Male_Artist class.\n
        Parameters:
        -----------
        - Artist Name: `str`
            The name of the artist.
        - Community Quiz ID: `str`
            The ID of the artist in the Community Quiz.
        """
        self.artist_name = artist_name
        self.community_quiz_id = community_quiz_id

    def __str__(self) -> str:
        """Return a string representation of the Male_Artist object. Use it to display male artist info in a compressed way (e.g. displaying info from all male artists)"""
        return f'{self.artist_name} - {self.community_quiz_id}'

    def __repr__(self) -> str:
        """Return a string representation of the Male_Artist object. Use it to display male artist info in a extended way (e.g. displaying info from only one male artist)"""
        male_artist = f'**Male Artist selected:** {self.artist_name}\n'
        male_artist += f'**Community Quiz ID:** {self.community_quiz_id}\n'
        return male_artist
    
class Male_VA:
    """Class that instanciates a Male VA object containing the information that is stored in the spotlight's sheet."""
    def __init__(self, artist_name: str, community_quiz_id: str) -> None:
        """
        Constructor of the Male_VA class.\n
        Parameters:
        -----------
        - Artist Name: `str`
            The name of the artist.
        - Community Quiz ID: `str`
            The ID of the artist in the Community Quiz.
        """
        self.artist_name = artist_name
        self.community_quiz_id = community_quiz_id

    def __str__(self) -> str:
        """Return a string representation of the Male_VA object. Use it to display male VA info in a compressed way (e.g. displaying info from all male artists)"""
        return f'{self.artist_name} - {self.community_quiz_id}'

    def __repr__(self) -> str:
        """Return a string representation of the Male_VA object. Use it to display male VA info in a extended way (e.g. displaying info from only one male artist)"""
        male_va = f'**Male VA selected:** {self.artist_name}\n'
        male_va += f'**Community Quiz ID:** {self.community_quiz_id}\n'
        return male_va
    
class Female_Artist:
    """Class that instanciates a Female Artist object containing the information that is stored in the spotlight's sheet."""
    def __init__(self, artist_name: str, community_quiz_id: str) -> None:
        """
        Constructor of the Female_Artist class.\n
        Parameters:
        -----------
        - Artist Name: `str`
            The name of the artist.
        - Community Quiz ID: `str`
            The ID of the artist in the Community Quiz.
        """
        self.artist_name = artist_name
        self.community_quiz_id = community_quiz_id

    def __str__(self) -> str:
        """Return a string representation of the Female_Artist object. Use it to display female artist info in a compressed way (e.g. displaying info from all female artists)"""
        return f'{self.artist_name} - {self.community_quiz_id}'

    def __repr__(self) -> str:
        """Return a string representation of the Female_Artist object. Use it to display female artist info in a extended way (e.g. displaying info from only one female artist)"""
        female_artist = f'**Female Artist selected:** {self.artist_name}\n'
        female_artist += f'**Community Quiz ID:** {self.community_quiz_id}\n'
        return female_artist
    
class Female_VA:
    """Class that instanciates a Female VA object containing the information that is stored in the spotlight's sheet."""
    def __init__(self, artist_name: str, community_quiz_id: str) -> None:
        """
        Constructor of the Female_VA class.\n
        Parameters:
        -----------
        - Artist Name: `str`
            The name of the artist.
        - Community Quiz ID: `str`
            The ID of the artist in the Community Quiz.
        """
        self.artist_name = artist_name
        self.community_quiz_id = community_quiz_id

    def __str__(self) -> str:
        """Return a string representation of the Female_VA object. Use it to display female VA info in a compressed way (e.g. displaying info from all female VAs)"""
        return f'{self.artist_name} - {self.community_quiz_id}'

    def __repr__(self) -> str:
        """Return a string representation of the Female_VA object. Use it to display female VA info in a extended way (e.g. displaying info from only one female VA)"""
        female_va = f'**Female VA selected:** {self.artist_name}\n'
        female_va += f'**Community Quiz ID:** {self.community_quiz_id}\n'
        return female_va
    
class Group:
    """Class that instanciates a Group object containing the information that is stored in the spotlight's sheet."""
    def __init__(self, group_name: str, community_quiz_id: str) -> None:
        """
        Constructor of the Group class.\n
        Parameters:
        -----------
        - Group Name: `str`
            The name of the group.
        - Community Quiz ID: `str`
            The ID of the group in the Community Quiz.
        """
        self.group_name = group_name
        self.community_quiz_id = community_quiz_id

    def __str__(self) -> str:
        """Return a string representation of the Group object. Use it to display group info in a compressed way (e.g. displaying info from all groups)"""
        return f'{self.group_name} - {self.community_quiz_id}'

    def __repr__(self) -> str:
        """Return a string representation of the Group object. Use it to display group info in a extended way (e.g. displaying info from only one group)"""
        group = f'**Group selected:** {self.group_name}\n'
        group += f'**Community Quiz ID:** {self.community_quiz_id}\n'
        return group
    
class Composer:
    """Class that instanciates a Composer object containing the information that is stored in the spotlight's sheet."""
    def __init__(self, composer_name: str, community_quiz_id: str) -> None:
        """
        Constructor of the Composer class.\n
        Parameters:
        -----------
        - Composer Name: `str`
            The name of the composer.
        - Community Quiz ID: `str`
            The ID of the composer in the Community Quiz.
        """
        self.composer_name = composer_name
        self.community_quiz_id = community_quiz_id

    def __str__(self) -> str:
        """Return a string representation of the Composer object. Use it to display composer info in a compressed way (e.g. displaying info from all composers)"""
        return f'{self.composer_name} - {self.community_quiz_id}'

    def __repr__(self) -> str:
        """Return a string representation of the Composer object. Use it to display composer info in a extended way (e.g. displaying info from only one composer)"""
        composer = f'**Composer selected:** {self.composer_name}\n'
        composer += f'**Community Quiz ID:** {self.community_quiz_id}\n'
        return composer
    
class Franchise:
    """Class that instanciates a Franchise object containing the information that is stored in the spotlight's sheet."""
    def __init__(self, franchise_name: str, community_quiz_id: str) -> None:
        """
        Constructor of the Franchise class.\n
        Parameters:
        -----------
        - Franchise Name: `str`
            The name of the franchise.
        - Community Quiz ID: `str`
            The ID of the franchise in the Community Quiz.
        """
        self.franchise_name = franchise_name
        self.community_quiz_id = community_quiz_id

    def __str__(self) -> str:
        """Return a string representation of the Franchise object. Use it to display franchise info in a compressed way (e.g. displaying info from all franchises)"""
        return f'{self.franchise_name} - {self.community_quiz_id}'

    def __repr__(self) -> str:
        """Return a string representation of the Franchise object. Use it to display franchise info in a extended way (e.g. displaying info from only one franchise)"""
        franchise = f'**Franchise selected:** {self.franchise_name}\n'
        franchise += f'**Community Quiz ID:** {self.community_quiz_id}\n'
        return franchise
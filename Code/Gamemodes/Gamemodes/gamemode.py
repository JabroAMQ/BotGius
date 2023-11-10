import random

class Gamemode:
    """Class that instanciates a Gamemode object containing the information that is stored in the database."""

    def __init__(
        self,
        gamemode_id : int,
        gamemode_name : str,
        gamemode_size : int,
        gamemode_code : str,
        watched_song_selection : bool,
        random_song_distribution : bool,
        weighted_song_distribution : bool,
        equal_song_distribution : bool,
        gamemode_info : str,
    ) -> None:
        """
        Constructor of the Gamemode class.

        Raises:
        -------
        `AssertionError` if:
        - Size: Lower than 1 or Greater than 8.
        - Song selection and Song Distribution: At least one possible Song Distribution if the Song Selection is watched (True) or None otherwise.
        """
        # Make sure the size value is possible
        assert gamemode_size >= 1 and gamemode_size <= 8

        # Make sure that if it is watched, there is at least one possible song distribution
        # Make sure that if it is not watched, all song distributions are False
        assert (watched_song_selection and (random_song_distribution or weighted_song_distribution or equal_song_distribution)) \
            or (not watched_song_selection and (not random_song_distribution and not weighted_song_distribution and not equal_song_distribution))

        self._id = gamemode_id
        self._name = gamemode_name
        self._size = gamemode_size
        self._code = gamemode_code
        self._info = gamemode_info
        self._watched_song_selection = watched_song_selection
        self._random_song_distribution = random_song_distribution
        self._weighted_song_distribution = weighted_song_distribution
        self._equal_song_distribution = equal_song_distribution

    
    @property
    def id(self) -> int:
        return self._id
    

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, new_name : str) -> None:
        self._name = new_name

    
    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, new_size : int) -> None:
        self._size = new_size


    @property
    def code(self) -> str:
        return self._code
    
    @code.setter
    def code(self, new_code : str) -> None:
        self._code = new_code
    

    @property
    def info(self) -> str:
        return self._info
    
    @info.setter
    def info(self, new_info : str) -> None:
        self._info = new_info


    @property
    def watched_song_selection(self) -> bool:
        return self._watched_song_selection

    @watched_song_selection.setter
    def watched_song_selection(self, new_watcehd_song_selection : bool) -> None:
        self._watched_song_selection = new_watcehd_song_selection


    @property
    def random_song_distribution(self) -> bool:
        return self._random_song_distribution
    
    @random_song_distribution.setter
    def random_song_distribution(self, new_random_song_distribution : bool) -> None:
        self._random_song_distribution = new_random_song_distribution
    

    @property
    def weighted_song_distribution(self) -> bool:
        return self._weighted_song_distribution
    
    @weighted_song_distribution.setter
    def weighted_song_distribution(self, new_weighted_song_distribution : bool) -> None:
        self._weighted_song_distribution = new_weighted_song_distribution

    
    @property
    def equal_song_distribution(self) -> bool:
        return self._equal_song_distribution
    
    @equal_song_distribution.setter
    def equal_song_distribution(self, new_equal_song_distribution : bool) -> None:
        self._equal_song_distribution = new_equal_song_distribution


    def _get_rollable_distributions(self) -> list[str]:
        """Return a list of strings with the possibles rollable song distributions available for the gamemode."""
        if not self.watched_song_selection:
            return ['Not Watched']
        
        rollable_distributions = []
        
        if self.random_song_distribution:
            rollable_distributions.append('Random')
        if self.weighted_song_distribution:
            rollable_distributions.append('Weighted')
        if self.equal_song_distribution:
            rollable_distributions.append('Equal')
        
        return rollable_distributions
    
    def roll_distribution(self) -> str:
        """Return one of the available song distributions of the gamemode."""
        distribution = random.choice(self._get_rollable_distributions())
        return f'(Distribution: {distribution})'


    def display_code_details(self) -> str:
        """Return the gamemode's code with some additional explanation about what it is being returned."""
        return f'This is the code for **{self.name}**:\n```{self.code}```'
    
    def display_info_details(self) -> str:
        """Return the gamemode's description and possible rollable distributiond with some additional explanation about what it is being returned."""
        if self.info:
            info_output = f'This is the info for **{self.name}**:\n{self.info}\n'
        else:
            info_output = f'{self.name} does not have description...\n'
        
        info_output += f'Rollable Distributions: {", ".join(self._get_rollable_distributions())}'
        return info_output
    
    def display_all_details(self) -> str:
        """Return a string with the gamemode's details (log utility)."""
        info = f'- **Name:** `{self.name}`.\n'
        info += f'- **Size:** `{self.size}v{self.size}` players.\n'
        info += f'- **Watched Song Selection:** `{self.watched_song_selection}`.\n'
        info += f'- **Random Song Distribution:** `{self.random_song_distribution}`.\n'
        info += f'- **Weighted Song Distribution:** `{self.weighted_song_distribution}`.\n'
        info += f'- **Equal Song Distribution:** `{self.equal_song_distribution}`.\n'
        info += f'- **Code:**\n```{self.code}```'
        return info


    def __eq__(self, other : object) -> bool:
        """
        Check whether 2 gamemodes are equal.\n
        Based on the gamemodes ids (database).
        """
        if not isinstance(other, Gamemode):
            return NotImplemented
        
        return self.id == other.id
    
    def __lt__(self, other : object) -> bool:
        """
        Check whether this gamemode is lower than another one.\n
        Based on the gamemode size and, if equal size, gamemode name (lowercase).
        """
        if not isinstance(other, Gamemode):
            return NotImplemented
        
        if self.size != other.size:
            return self.size < other.size
        
        return self.name.lower() < other.name.lower()
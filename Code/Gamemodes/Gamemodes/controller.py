import difflib

from Code.Utilities.error_handler import print_exception
from Code.Gamemodes.Gamemodes.database import Gamemodes_Database
from Code.Gamemodes.Gamemodes.gamemode import Gamemode

class Gamemodes_Controller:
    """Controller to encapsule the Gamemodes Logic from the rest of the application."""

    def __init__(self, gamemodes_descriptions: dict[str, str]) -> None:
        """Retrieve all the Gamemodes from the Database and load them into memory through the Gamemodes's Catalogs (by id and name)."""
        self.gamemodes_by_ids: dict[int, Gamemode] = {}
        self.gamemodes_by_names: dict[str, Gamemode] = {}

        for gamemode_data in Gamemodes_Database.get_all_gamemodes():
            name = gamemode_data[0]
            description = gamemodes_descriptions.get(name.lower(), '')
            self._add_gamemode_to_catalogs(*gamemode_data, description)
            if not description:
                print(f'Description for gamemode {name} couldn\'t be retrieved from the sheet!')


    def _add_gamemode_to_catalogs(
        self,
        gamemode_name: str,
        gamemode_size: int,
        gamemode_code: str,
        is_gamemode_watched: bool,
        is_random_dist_rollable: bool,
        is_weighted_dist_rollable: bool,
        is_equal_dist_rollable: bool,
        gamemode_id: int,
        gamemode_description: str
    ) -> None:
        """Create the gamemode given its data and store it in the Gamemodes catalogs (by id and name (lowercase))."""
        try:
            new_gamemode = Gamemode(
                gamemode_id=gamemode_id,
                gamemode_name=gamemode_name,
                gamemode_size=gamemode_size,
                gamemode_code=gamemode_code,
                watched_song_selection=is_gamemode_watched,
                random_song_distribution=is_random_dist_rollable,
                weighted_song_distribution=is_weighted_dist_rollable,
                equal_song_distribution=is_equal_dist_rollable,
                gamemode_info=gamemode_description
            )

        except AssertionError:
            print(f'Gamemode {gamemode_name} couldn\'t be added to the catalogs as it contains invalid values!')
            return
        
        self.gamemodes_by_ids[gamemode_id] = new_gamemode
        self.gamemodes_by_names[gamemode_name.lower()] = new_gamemode


    def _get_gamemode_by_name(self, gamemode_name: str) -> Gamemode | None:
        """Return the gamemode which name is the most similar to the `gamemode_name` provided as argument (or None if a not close enough match was found)."""
        closest_matches = difflib.get_close_matches(gamemode_name.lower(), self.gamemodes_by_names.keys())
        closest_match = closest_matches[0] if closest_matches else None
        return self.gamemodes_by_names.get(closest_match) if closest_match is not None else None
    
    def get_gamemode(self, gamemode: int | str) -> Gamemode | None:
        """
        Return the gamemode based on either the name or the id provided as argument.\n
        If a string is provided as argument, the gamemode with the closest match to the name provided will be returned.\n
        `None` can be returned if a not similar enough match couldn't be found (`str` case) or if the ID wasn't found in the catalog (`int` case).

        Raises:
        -----------
        - `ValueError`: If a not int or string type is provided as argument.
        """
        if isinstance(gamemode, int):
            return self.gamemodes_by_ids.get(gamemode)
        elif isinstance(gamemode, str):
            return self._get_gamemode_by_name(gamemode)
        else:
            return ValueError('Invalid argument type provided.')
    
    def get_all_gamemodes(self) -> list[Gamemode]:
        """Return a list containing all the gamemodes."""
        return list(self.gamemodes_by_ids.values())


    def list_all_gamemodes(self) -> list[str]:
        """
        Return a list of strings, each of them consisting in a gamemode name (or a string that split the gamemodes by size ("1v1 Gamemodes", "2v2 Gamemodes", etc.)) ordered as follow:
        - `Size`: Gamemodes with less players required per team goes first
        - `Name`: If same size, they are ordered by the gamemode's name (not case sensitive)
        """
        current_size = 0
        sorted_gamemodes = []

        for gamemode in sorted(self.gamemodes_by_ids.values()):
            if gamemode.size > current_size:
                sorted_gamemodes.append(f'\n**{gamemode.size}vs{gamemode.size} players:**')
                current_size = gamemode.size
            sorted_gamemodes.append(gamemode.name)
        
        return sorted_gamemodes


    def _ensure_valid_gamemode_values(
        self,
        watched_song_selection: bool,
        random_song_distribution: bool,
        weighted_song_distribution: bool,
        equal_song_distribution: bool
    ) -> tuple[bool, bool, bool, bool]:
        """Method that make sure that gamemode fields's values are valid, modifying them accordingly in order to ensure this."""
        # Make sure that watched distributions are False if song distribution is not watched (or hybrid)
        if not watched_song_selection:
            random_song_distribution, weighted_song_distribution, equal_song_distribution = (False for _ in range(3))
        
        # Make sure that there is at least one rollable distribution if song distribution is watched (or hybrid)
        elif watched_song_selection and not (random_song_distribution or weighted_song_distribution or equal_song_distribution):
            random_song_distribution = True  # Set random distribution to rollable by default if none distribution is rollable (for watched song selection gamemodes).

        return watched_song_selection, random_song_distribution, weighted_song_distribution, equal_song_distribution


    def add_gamemode(
        self,
        gamemode_name: str,
        gamemode_size: int,
        gamemode_code: str,
        is_watched: bool,
        is_random_dist_rollable: bool,
        is_weighted_dist_rollable: bool,
        is_equal_dist_rollable: bool
    ) -> tuple[bool, str]:
        """
        Create a gamemode with the provided data, storing it into the database and memory (through the gamemodes's catalogs).\n
        Return a tuple consisting of 2 values:
        - A boolean which is `True` if the gamemode could be stored, `False` otherwise, this is, a gamemode with that name already existed in memory.
        - A log str providing the gamemode's data.
        """
        # Check that a gamemode with that name is not already stored in the catalog
        if self.gamemodes_by_names.get(gamemode_name.lower()):
            return False, None
        
        # Modify watched song distribution values in case they are invalid
        is_watched, is_random_dist_rollable, is_weighted_dist_rollable, is_equal_dist_rollable = self._ensure_valid_gamemode_values(
            watched_song_selection=is_watched,
            random_song_distribution=is_random_dist_rollable,
            weighted_song_distribution=is_weighted_dist_rollable,
            equal_song_distribution=is_equal_dist_rollable
        )

        # Add the gamemode to the database
        gamemode_id = Gamemodes_Database.add_gamemode(
            name=gamemode_name,
            size=gamemode_size,
            code=gamemode_code,
            watched_song_selection=is_watched,
            random_song_distribution=is_random_dist_rollable,
            weighted_song_distribution=is_weighted_dist_rollable,
            equal_song_distribution=is_equal_dist_rollable
        )

        # Add the gameomde to the catalogs
        self._add_gamemode_to_catalogs(
            gamemode_id=gamemode_id,
            gamemode_name=gamemode_name,
            gamemode_size=gamemode_size,
            gamemode_code=gamemode_code,
            gamemode_description=None,
            is_gamemode_watched=is_watched,
            is_random_dist_rollable=is_random_dist_rollable,
            is_weighted_dist_rollable=is_weighted_dist_rollable,
            is_equal_dist_rollable=is_equal_dist_rollable
        )

        # Get the log message (information about the gamemode created)
        gamemode = self.gamemodes_by_ids.get(gamemode_id)
        log_message = gamemode.display_all_details()
        return True, log_message


    def delete_gamemode(self, gamemode: Gamemode) -> bool:
        """
        Delete the gamemode provided as argument from the database and the catalogs.\n
        Return `True` if the gamemode was deleted successfully, `False` otherwise.
        """
        try:
            Gamemodes_Database.delete_gamemode(gamemode.name)
            del self.gamemodes_by_ids[gamemode.id]
            del self.gamemodes_by_names[gamemode.name.lower()]
            return True
        
        except Exception as error:
            print_exception(error)
            return False


    def get_gamemode_old_values(
        self,
        gamemode: Gamemode,
        new_name: str | None,
        new_code: str | None,
        new_random: bool | None,
        new_weighted: bool | None,
        new_equal: bool | None
    ) -> tuple[bool, str | None, str | None, bool | None, bool | None, bool | None]:
        """
        For each of the gamemode fields editable (those that have a parameter in this function), return `None` if a new value wasn't provided or if the new
        value is the same as the field currently contained. It return the old value of the field otherwise (this is, a change was made).\n
        It also return as the first tuple value a boolean that indicate whether there is an invalid combination of field values.
        """
        name = gamemode.name if new_name is not None and new_name != gamemode.name else None
        code = gamemode.code if new_code is not None and new_code != gamemode.code else None
        random = gamemode.random_song_distribution if new_random is not None and new_random != gamemode.random_song_distribution else None
        weighted = gamemode.weighted_song_distribution if new_weighted is not None and new_weighted != gamemode.weighted_song_distribution else None
        equal = gamemode.equal_song_distribution if new_equal is not None and new_equal != gamemode.equal_song_distribution else None

        invalid = False
        # For watched gamemodes, check if a distribution has been changed from True to False.
        if gamemode.watched_song_selection:
            # Make sure that there is at least one distribution that is stil True after the changes
            if random is not None and not new_random and not gamemode.weighted_song_distribution and not gamemode.equal_song_distribution:
                invalid = True
            if weighted is not None and not new_weighted and not gamemode.random_song_distribution and not gamemode.equal_song_distribution:
                invalid = True
            if equal is not None and not new_equal and not gamemode.random_song_distribution and not gamemode.weighted_song_distribution:
                invalid = True

        return invalid, name, code, random, weighted, equal

    def edit_gamemode(
        self,
        gamemode_name: str,
        new_name: str | None,
        new_code: str | None,
        new_random: bool | None,
        new_weighted: bool | None,
        new_equal: bool | None
    ) -> bool:
        """
        Edit the gamemode with name `gamemode_name`.
        If a `new_...` field is `None` it will be ignored, this is, it won't be modified.
        Return `True` if changes could be applied and `False` if an error was raised when applying the changes in the database.
        """
        gamemode = self.gamemodes_by_names.get(gamemode_name.lower())

        new_name = new_name if new_name is not None else gamemode.name
        new_code = new_code if new_code is not None else gamemode.code
        new_random = new_random if new_random is not None else gamemode.random_song_distribution
        new_weighted = new_weighted if new_weighted is not None else gamemode.weighted_song_distribution
        new_equal = new_equal if new_equal is not None else gamemode.equal_song_distribution

        try:
            Gamemodes_Database.edit_gamemode(
                id=gamemode.id,
                new_name=new_name,
                new_code=new_code,
                new_random_song_distribution=new_random,
                new_weighted_song_distribution=new_weighted,
                new_equal_song_distribution=new_equal
            )

            # deleting (or modifying the values) from gamemodes_by_ids catalog is not needed
            del self.gamemodes_by_names[gamemode.name.lower()]

            gamemode.name = new_name
            gamemode.code = new_code
            gamemode.random_song_distribution = new_random
            gamemode.weighted_song_distribution = new_weighted
            gamemode.equal_song_distribution = new_equal

            self.gamemodes_by_names[new_name.lower()] = gamemode
            return True
        
        except Exception as error:
            print_exception(error)
            return False
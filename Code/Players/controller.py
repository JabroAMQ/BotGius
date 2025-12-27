import difflib

import discord

from Code.Players.player import Player
from Code.Players.database_sqlite3 import Players_Database
from Code.Gamemodes.Gamemodes.gamemode import Gamemode

class Players_Controller:
    """Controller to encapsule the Players Logic from the rest of the application."""
    _instance = None
    def __new__(cls) -> None:
        """Override the __new__ method to return the existing instance of the class if it exists or create a new instance if it doesn't exist yet.\n"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance
    
    def _set_data(self) -> None:
        """Retrieve all the Players from the Database and load them into memory through the Players's Catalogs (by id and amq_name)."""
        self.players_by_ids: dict[int, Player] = {}
        self.players_by_amq_name: dict[str, Player] = {}

        players = Players_Database.get_all_players()
        for player_data in players:
            self._add_player_to_catalogs(*player_data)


    def _add_player_to_catalogs(self, discord_id: int, amq_name: str, rank: str = 'None', is_banned: bool = False, is_list_banned: bool = False) -> None:
        """Add a player to the Players's Catalogs (by `discord_id` and `amq_name`)."""
        player = Player(discord_id=discord_id, amq_name=amq_name, rank=rank, is_banned=is_banned, is_list_banned=is_list_banned)
        self.players_by_ids[discord_id] = player
        self.players_by_amq_name[amq_name.lower()] = player
    

    def _get_player_by_name(self, amq_name: str) -> Player | None:
        """Return the player which name is the most similar to the `amq_name` provided as argument (or None if a not close enough match was found)."""
        closest_matches = difflib.get_close_matches(amq_name.lower(), self.players_by_amq_name.keys())
        closest_match = closest_matches[0] if closest_matches else None
        return self.players_by_amq_name.get(closest_match) if closest_match is not None else None

    def get_player(self, id_or_name: int | str) -> Player | None:
        """
        Return the `Player` object given its `discord_id` or `amq_name`.\n
        `None` will be returned if the `discord_id` or `amq_name` provided wasn't found in the database.

        Raise:
        ------
        - `ValueError`:
            If the `id_or_name` value provided is not a `int` or a `str`.
        """
        if isinstance(id_or_name, int):
            return self.players_by_ids.get(id_or_name)
        
        elif isinstance(id_or_name, str):
            return self._get_player_by_name(id_or_name)
        
        else:
            raise ValueError('Invalid `id_or_name` value type!')


    def get_player_from_discord_name(self, guild: discord.Guild, discord_name: str) -> Player | None:
        """Return the `Player` object associated to the discord account which has the closest name to `discord_name` among all the `guild`'s members."""
        possibilities = {}
        for member in guild.members:
            possibilities[member.name.lower()] = member.id
            if member.nick:
                possibilities[member.nick.lower()] = member.id
            if member.global_name:
                possibilities[member.global_name.lower()] = member.id
        
        closest_matches = difflib.get_close_matches(discord_name.lower(), possibilities.keys())
        closest_match = closest_matches[0] if closest_matches else None
        
        if closest_match is None:
            return None

        discord_id = possibilities.get(closest_match)
        return self.players_by_ids.get(discord_id) if discord_id is not None else None

    
    def get_all_banned_players(self) -> list[Player]:
        """Return a list wirh all the players that are currently banned."""
        return [player for player in self.players_by_ids.values() if player.is_banned]
    
    def get_all_list_banned_players(self) -> list[Player]:
        """Return a list wirh all the players that are currently list banned."""
        return [player for player in self.players_by_ids.values() if player.is_list_banned]


    def register_player(self, discord_id: int, amq_name: str) -> tuple[bool, str | None]:
        """
        Add a player to the Players's Database and Catalogs (by `discord_id` and `amq_name`).\n
        Only `discord_id` and `amq_name` are required as the rest of the Player's fields will be initialized as the default values.\n
        Return a tuple consisting of:
        - A boolean telling whether the player could be added to the Players's database and catalogs.
        - A str with the ping of the player that is currently using `amq_name` as their amq name, or `None` if `amq_name` is free to be used.
        """
        # Check if user is already registered
        if self.players_by_ids.get(discord_id):
            return False, None
        
        # Check if amq_name is already used by another player
        other_player = self.players_by_amq_name.get(amq_name.lower())
        if other_player is not None:
            return False, other_player.discord_ping

        self._add_player_to_catalogs(discord_id, amq_name)
        Players_Database.add_player(discord_id, amq_name)
        return True, None


    def change_player_amq(self, discord_id: int, new_amq_name: str) -> tuple[bool, str | None]:
        """
        Change the player's amq name with `discord_id` to `new_amq_name`.\n
        The method return a tuple which first element is a boolean that can be `False` if:
        - The discord user is not registered in the Players's Database (`discord_id` not found).
        - The `new_amq_name` chosen is already used by other player.\n
        The method also return a string which consists of:
        - The old amq name that the player used to have if the change could be successfully applied (log).
        - The discord ping of the player that is currently using `new_amq_name` as their amq_name, or `None` if the name is free to be used.
        """
        player = self.players_by_ids.get(discord_id)
        # Check if the player is registered in the database
        if player is None:
            return False, None

        # Check if the new name chosen is free
        other_player = self.players_by_amq_name.get(new_amq_name.lower())
        if other_player is not None:
            return False, other_player.discord_ping
        
        # Delete old references (deleting (or modifying the amq name value) from player_by_ids catalog is not needed)
        del self.players_by_amq_name[player.amq_name.lower()]

        # Change the name and reinsert the Player in the catalogs with their new name
        old_amq_name = player.amq_name
        player.amq_name = new_amq_name
        self.players_by_amq_name[player.amq_name.lower()] = player

        # Apply the change into the database
        Players_Database.change_player_amq(player.discord_id, player.amq_name)
        return True, old_amq_name
    

    def change_player_rank(self, player_amq_name: str, new_rank: str) -> tuple[bool, Player, str]:
        """
        Change the rank of the player with name == `player_amq_name`.\n
        Returns a boolean telling the user whether the change could be applied.\n
        It also return the player object and the old rank that the player used to have (log values). 
        """
        # Get the player from name
        player = self._get_player_by_name(player_amq_name)
        if player is None:
            return False, None, ''
        
        # Update rank in memory
        old_rank = player.rank.name
        player.rank = new_rank

        # Update rank in database
        Players_Database.change_player_rank(player.discord_id, player.rank.name)

        return True, player, old_rank
    

    def change_player_ban(self, player_amq_name: str, new_is_banned: bool) -> tuple[bool, bool, Player | None]:
        """
        Change the `is_banned` value of the player with name == `player_amq_name`.\n
        Returns a tuple:
        - 1: Whether a player with `player_amq_name` name was found.
        - 2: Whether the changes could be applied (if the `is_banned` value stored was not `new_is_banned` already).
        - 3: The player whom changes were applied to.
        """
        # Get the player from name
        player = self._get_player_by_name(player_amq_name)
        if player is None:
            return False, False, None
        
        # Check if new is_banned value is already the one stored
        if new_is_banned == player.is_banned:
            return True, False, player
        
        # Update is_banned in memory
        player.is_banned = new_is_banned

        # Update is_banned in database
        Players_Database.change_is_baned(player.discord_id, player.is_banned)

        return True, True, player
    

    def change_player_list_ban(self, player_amq_name: str, new_is_list_banned: bool) -> tuple[bool, bool, Player | None]:
        """
        Change the `is_list_banned` value of the player with name == `player_amq_name`.\n
        Returns a tuple:
        - 1: Whether a player with `player_amq_name` name was found.
        - 2: Whether the changes could be applied (if the `is_list_banned` value stored was not `new_is_list_banned` already).
        - 3: The player whom changes were applied to.
        """
        # Get the player from name
        player = self._get_player_by_name(player_amq_name)
        if player is None:
            return False, False, None

        # Check if new is_list_banned value is already the one stored
        if new_is_list_banned == player.is_list_banned:
            return True, False, player
        
        # Update is_list_banned in memory
        player.is_list_banned = new_is_list_banned

        # Update is_list_banned in database
        Players_Database.change_is_list_baned(player.discord_id, player.is_list_banned)

        return True, True, player
from copy import copy

import discord

class Rank:
    """Class to represent a possible player' rank."""
    def __init__(self, rank_name: str, rank_value: int) -> None:
        self._name = rank_name
        self._value = rank_value

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def value(self) -> int:
        return self._value
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rank):
            return NotImplemented
        return self.value == other.value
    
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Rank):
            return NotImplemented
        return self.value < other.value
    
    def __add__(self, other: object) -> int:
        if not isinstance(other, Rank):
            return NotImplemented
        return self.value + other.value


class Ranking:
    """Class which contains all the possible player's ranks."""
    _instance = None
    def __new__(cls) -> None:
        """Override the __new__ method to return the existing instance of the class if it exists or create a new instance if it doesn't exist yet.\n"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance
    
    def _set_data(self) -> None:

        # NOTE Ideally this should be an Enum class but '+' or '-' can't be set as part of a variable name...
        self.rank_names = [
            'Anything Goes',
            'Ubers',
            'SS+', 'SS', 'SS-',
            'S+', 'S', 'S-',
            'A+', 'A', 'A-',
            'B+', 'B', 'B-',
            'C+', 'C', 'C-',
            'D+', 'D', 'D-',
            'None'
        ]
        
        self.ranks_by_names = {
            name: Rank(rank_name=name, rank_value=value+1)
            for value, name in enumerate(self.rank_names)
        }
        self.ranks_by_values = {
            value: Rank(rank_name=name, rank_value=value+1)
            for value, name in enumerate(self.rank_names)
        }


    def get_rank(self, rank_name: str) -> Rank:
        """
        Return the `Rank` object with name == `rank_name`.\n
        In case that no rank with name `rank_name` is found, the default Rank "None" will be returned instead.
        """
        rank = self.ranks_by_names.get(rank_name)
        return rank if rank is not None else self.ranks_by_names['None']
    

    def get_rank_embed(self, guild: discord.Guild, rank_value: int) -> tuple[discord.Embed, int]:
        """
        Return:
        - A discord Embed containing the rank name and all the players with that rank.
        - The `rank_value`, which value can be modified if the provided one was invalid.
        """
        # importing inside function to avoid circular import error
        from Code.Players.controller import Players_Controller

        # Ensure rank_value is valid  
        min_value, max_value = 0, len(self.ranks_by_values) - 1
        if rank_value < min_value:
            rank_value = max_value      # The next of the last is the first
        if rank_value > max_value:
            rank_value = min_value      # The previous of the first is the last

        # Get the rank
        selected_rank = self.ranks_by_values[rank_value]

        # Get all the players with rank == rank_value
        all_players = list(Players_Controller().players_by_amq_name.values())
        all_players_in_rank = filter(lambda player: player.rank == selected_rank, all_players)

        # Sort the players
        all_players_in_rank = sorted(list(all_players_in_rank))

        # Get all the players identification: "amq_name (discord_user)"
        all_discords_in_rank: list[discord.Member] = []
        all_players_in_rank_copy = copy(all_players_in_rank)

        # NOTE we don't show those players who left the server (not present in the guild where the command is being executed)
        for player in all_players_in_rank_copy:
            member = guild.get_member(player.discord_id)
            if member is not None:
                all_discords_in_rank.append(member)
            else:
                all_players_in_rank.remove(player)

        all_names_in_rank = [
            f'**{discord.utils.escape_markdown(player.amq_name)}** ({discord.utils.escape_markdown(discord_member.display_name)})'
            for player, discord_member in zip(all_players_in_rank, all_discords_in_rank)
        ]

        # Create the embed
        embed = discord.Embed(title=selected_rank.name, description='\n'.join(all_names_in_rank), colour=discord.Colour.green())
        embed.set_footer(text=f'Page {rank_value+1} / {max_value+1}')

        return embed, rank_value
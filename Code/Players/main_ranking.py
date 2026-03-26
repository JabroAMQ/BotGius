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
        return self.value > other.value
    
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
            'F',
            'EMQ', 'None'
        ]
        # NOTE we have to reverse rank values to make sure Anything Goes has the highest value and None the lowest one
        reversed_ranks = self.rank_names[::-1]

        self.ranks_by_names = {
            name: Rank(rank_name=name, rank_value=value+1)
            for value, name in enumerate(reversed_ranks)
        }
        self.ranks_by_values = {
            rank.value: rank
            for rank in self.ranks_by_names.values()
        }


    def get_rank(self, rank_name: str) -> Rank:
        """
        Return the `Rank` object with name == `rank_name`.\n
        In case that no rank with name `rank_name` is found, the default Rank "None" will be returned instead.
        """
        rank = self.ranks_by_names.get(rank_name)
        return rank if rank is not None else self.ranks_by_names['None']
    

    def get_rank_embed(self, guild: discord.Guild, page: int) -> tuple[discord.Embed, int]:
        """
        Return:
        - A discord Embed containing the rank name and all the players with that rank.
        - The `rank_value`, which value can be modified if the provided one was invalid.
        """
        # Importing inside function to avoid circular import error
        from Code.Players.controller import Players_Controller

        # Wrap-around logic for the UI pages (1-23)
        total_ranks = len(self.rank_names)
        if page < 1: page = total_ranks
        if page > total_ranks: page = 1
        
        # Map Page 1 -> Anything Goes (Index 0 in rank_names list)
        rank_name = self.rank_names[page - 1]
        selected_rank = self.ranks_by_names[rank_name]
        
        # Filter players
        all_players = Players_Controller().players_by_amq_name.values()
        valid_entries = []
        for player in sorted(all_players):
            if player.rank == selected_rank:
                member = guild.get_member(player.discord_id)
                if member:
                    name = discord.utils.escape_markdown(player.amq_name)
                    display = discord.utils.escape_markdown(member.display_name)
                    valid_entries.append(f'**{name}** ({display})')

        embed = discord.Embed(
            title=selected_rank.name,
            description='\n'.join(valid_entries),
            colour=discord.Colour.green()
        )
        embed.set_footer(text=f'Page {page} / {total_ranks}')

        # Return the validated page number to keep the View in sync
        return embed, page
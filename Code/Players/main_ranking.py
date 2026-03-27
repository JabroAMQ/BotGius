from copy import copy

import discord

class Rank:
    """Class to represent a possible player' rank."""
    def __init__(self, rank_name: str, rank_position: int, rank_value: int) -> None:
        self._name = rank_name
        self._position = rank_position
        self._value = rank_value

    @property
    def name(self) -> str:
        return self._name

    @property
    def position(self) -> int:
        return self._position

    @property
    def value(self) -> int:
        return self._value
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rank):
            return NotImplemented
        return self.position == other.position
    
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Rank):
            return NotImplemented
        return self.position < other.position
    
    def __add__(self, other: object) -> int:
        if not isinstance(other, Rank):
            return NotImplemented
        return self.value + other.value


class Ranking:
    """Class which contains all the possible player's ranks."""
    _instance = None
    # NOTE Keep the ranks ordered from the highest to the lowest, as the position is used to order the ranks
    _RANKS: list[tuple[str, int]] = [
        ('Anything Goes', 23),
        ('Ubers', 21),
        ('SS+', 19),
        ('SS', 18),
        ('SS-', 17),
        ('S+', 16),
        ('S', 15),
        ('S-', 14),
        ('A+', 13),
        ('A', 12),
        ('A-', 11),
        ('B+', 10),
        ('B', 9),
        ('B-', 8),
        ('C+', 7),
        ('C', 6),
        ('C-', 5),
        ('D+', 4),
        ('D', 3),
        ('D-', 2),
        ('F', 1),
        ('EMQ', 0),
        ('None', 0)
    ]
    
    def __new__(cls) -> 'Ranking':
        """Override the __new__ method to return the existing instance of the class if it exists or create a new instance if it doesn't exist yet.\n"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance
    
    def _set_data(self) -> None:
        self.rank_names = []
        self.ranks_by_names = {}
        self.rank_by_positions = {}

        for rank_position, (rank_name, rank_value) in enumerate(self._RANKS):
            rank = Rank(rank_name, rank_position, rank_value)
            self.rank_names.append(rank_name)
            self.ranks_by_names[rank_name] = rank
            self.rank_by_positions[rank_position] = rank


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

        # Wrap-around logic for the UI pages
        total_ranks = len(self.rank_names)
        if page < 0: page = total_ranks-1
        if page >= total_ranks: page = 0
        selected_rank = self.rank_by_positions[page]
        
        # Filter players
        all_players = Players_Controller().players_by_amq_name.values()
        valid_entries = []
        for player in sorted(all_players):
            if player.rank == selected_rank:
                # We show only the players that are in the guild where the command was executed
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
        embed.set_footer(text=f'Page {page+1} / {total_ranks}')

        # Return the validated page number to keep the View in sync
        return embed, page
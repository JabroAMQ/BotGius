import discord

from Code.Players.main_ranking import Ranking, Rank
from Code.Gamemodes.controller import Main_Controller as Gamemodes_Controller
from Code.Gamemodes.Gamemodes.gamemode import Gamemode

class Player:
    """Class that instanciates a Player object containing the information that is stored in the database."""

    def __init__(self, discord_id: int, amq_name: str, rank: str = 'None', is_banned: bool = False) -> None:
        """Constructor of the Player class."""
        self._discord_id = discord_id
        self._amq_name = amq_name
        self._rank = rank
        self._is_banned = is_banned

    # No setter, final
    @property
    def discord_id(self) -> int:
        return self._discord_id
    
    # No setter, calculated from discord_id
    @property
    def discord_ping(self) -> str:
        return f'<@{self.discord_id}>'
    
    @property
    def amq_name(self) -> str:
        return self._amq_name
    
    @amq_name.setter
    def amq_name(self, new_amq_name: str) -> None:
        self._amq_name = new_amq_name

    @property
    def rank(self) -> Rank:
        return Ranking().get_rank(self._rank)
    
    @rank.setter
    def rank(self, new_rank: str) -> None:
        self._rank = new_rank
    
    @property
    def is_banned(self) -> bool:
        return self._is_banned
    
    @is_banned.setter
    def is_banned(self, new_is_banned: bool) -> None:
        self._is_banned = new_is_banned


    async def get_profile_embed(self, client: discord.Client) -> discord.Embed:
        """Returns a discord Embed containing the profile page of the Player."""
        embed = discord.Embed(title=self.amq_name, color=discord.Colour.green())
        embed_user = await client.fetch_user(self.discord_id)
        embed_url = 'https://animemusicquiz.com'
        embed_icon_url = 'https://animemusicquiz.com/favicon-32x32.png'

        embed_name = 'Profile'
        embed.add_field(name='Discord', value=embed_user.display_name, inline=False)
        embed.add_field(name='Rank', value=self.rank.name, inline=False)
        embed.add_field(name='Elo', value='To Be Determined', inline=False)
        embed.set_thumbnail(url=embed_user.display_avatar.url)

        embed.set_author(name=embed_name, url=embed_url, icon_url=embed_icon_url)
        return embed


    def __eq__(self, other: object) -> bool:
        """
        Check whether 2 players are equal.\n
        Based on the players ids (database).
        """
        if not isinstance(other, Player):
            return NotImplemented
        
        return self.discord_id == other.discord_id
    
    def __lt__(self, other: object) -> bool:
        """
        Check whether this player is lower than another one.\n
        Based on player rank and, in case of same rank, name (lowercase).
        """
        if not isinstance(other, Player):
            return NotImplemented
        
        if self.rank < other.rank:
            return True
        if self.rank > other.rank:
            return False
        
        return self.amq_name.lower() < other.amq_name.lower()
    

    def __add__(self, other: object) -> int:
        """
        Define addition for Player object.\n
        Based on Rank value.
        """
        if not isinstance(other, Player):
            return NotImplemented
        
        return self.rank + other.rank
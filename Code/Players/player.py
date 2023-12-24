import discord

from Code.Players.main_ranking import Ranking, Rank
from Code.Gamemodes.controller import Main_Controller as Gamemodes_Controller
from Code.Gamemodes.Gamemodes.gamemode import Gamemode

class Player:
    """Class that instanciates a Player object containing the information that is stored in the database."""

    def __init__(
        self,
        discord_id: int,
        amq_name: str,
        rank: str = 'None',
        elo: int = 0,
        list_name: str = 'TBD',
        list_from: str = 'TBD',
        list_sections: str = 'TBD',
        fav_1v1_gamemode_id: int = None,
        hated_1v1_gamemode_id: int = None,
        fav_2v2_gamemode_id: int = None,
        hated_2v2_gamemode_id: int = None,
        fav_4v4_gamemode_id: int = None,
        hated_4v4_gamemode_id: int = None,
        is_banned: bool = False
    ) -> None:
        """Constructor of the Player class."""
        self._discord_id = discord_id
        self._amq_name = amq_name

        self._elo = elo     # Unused
        self._rank = rank
        self._is_banned = is_banned
        
        self._list_name = list_name
        self._list_from = list_from
        self._list_sections = list_sections

        self._fav_1v1_gamemode_id = fav_1v1_gamemode_id
        self._fav_2v2_gamemode_id = fav_2v2_gamemode_id
        self._fav_4v4_gamemode_id = fav_4v4_gamemode_id
        self._hated_1v1_gamemode_id = hated_1v1_gamemode_id
        self._hated_2v2_gamemode_id = hated_2v2_gamemode_id
        self._hated_4v4_gamemode_id = hated_4v4_gamemode_id


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
    

    @property
    def list_name(self) -> str:
        return self._list_name
    
    @list_name.setter
    def list_name(self, new_list_name: str) -> None:
        self._list_name = new_list_name

    @property
    def list_from(self) -> str:
        return self._list_from
    
    @list_from.setter
    def list_from(self, new_list_from: str) -> None:
        self._list_from = new_list_from

    @property
    def list_sections(self) -> str:
        return self._list_sections
    
    @list_sections.setter
    def list_sections(self, new_list_sections: str) -> None:
        self._list_sections = new_list_sections

    @property
    def fav_1v1_gamemode(self) -> Gamemode | None:
        return Gamemodes_Controller().get_gamemode(self._fav_1v1_gamemode_id) if self._fav_1v1_gamemode_id is not None else None
    
    @fav_1v1_gamemode.setter
    def fav_1v1_gamemode(self, new_fav_1v1_gamemode_id: int) -> None:
        self._fav_1v1_gamemode_id = new_fav_1v1_gamemode_id

    @property
    def fav_2v2_gamemode(self) -> Gamemode | None:
        return Gamemodes_Controller().get_gamemode(self._fav_2v2_gamemode_id) if self._fav_2v2_gamemode_id is not None else None
    
    @fav_2v2_gamemode.setter
    def fav_2v2_gamemode(self, new_fav_2v2_gamemode_id: int) -> None:
        self._fav_2v2_gamemode_id = new_fav_2v2_gamemode_id

    @property
    def fav_4v4_gamemode(self) -> Gamemode | None:
        return Gamemodes_Controller().get_gamemode(self._fav_4v4_gamemode_id) if self._fav_4v4_gamemode_id is not None else None
    
    @fav_4v4_gamemode.setter
    def fav_4v4_gamemode(self, new_fav_4v4_gamemode_id: int) -> None:
        self._fav_4v4_gamemode_id = new_fav_4v4_gamemode_id

    @property
    def hated_1v1_gamemode(self) -> Gamemode | None:
        return Gamemodes_Controller().get_gamemode(self._hated_1v1_gamemode_id) if self._hated_1v1_gamemode_id is not None else None
    
    @hated_1v1_gamemode.setter
    def hated_1v1_gamemode(self, new_hated_1v1_gamemode_id: int) -> None:
        self._hated_1v1_gamemode_id = new_hated_1v1_gamemode_id

    @property
    def hated_2v2_gamemode(self) -> Gamemode | None:
        return Gamemodes_Controller().get_gamemode(self._hated_2v2_gamemode_id) if self._hated_2v2_gamemode_id is not None else None
    
    @hated_2v2_gamemode.setter
    def hated_2v2_gamemode(self, new_hated_2v2_gamemode_id: int) -> None:
        self._hated_2v2_gamemode_id = new_hated_2v2_gamemode_id

    @property
    def hated_4v4_gamemode(self) -> Gamemode | None:
        return Gamemodes_Controller().get_gamemode(self._hated_4v4_gamemode_id) if self._hated_4v4_gamemode_id is not None else None
    
    @hated_4v4_gamemode.setter
    def hated_4v4_gamemode(self, new_hated_4v4_gamemode_id: int) -> None:
        self._hated_4v4_gamemode_id = new_hated_4v4_gamemode_id


    def display_list_info(self) -> str:
        """Return a string with the player's list information information (log utility, for getting only the values use `get_list_info()` instead)."""
        info = f'- List name: **{self.list_name}**\n'
        info += f'- List from: **{self.list_from}**\n'
        info += f'- List sections: **{self.list_sections}**'
        return info

    def display_gamemodes_info(self) -> str:
        """Return a string with the player's prefered gamemodes information (log utility, for getting only the values use `get_gamemodes_info()` instead)."""
        info = f'- **Favourite 1v1 Gamemode:** {self.fav_1v1_gamemode.name if self.fav_1v1_gamemode is not None else None}\n'
        info += f'- **Favourite 2v2 Gamemode:** {self.fav_2v2_gamemode.name if self.fav_2v2_gamemode is not None else None}\n'
        info += f'- **Favourite 4v4 Gamemode:** {self.fav_4v4_gamemode.name if self.fav_4v4_gamemode is not None else None}\n'
        info += f'- **Hated 1v1 Gamemode:** {self.hated_1v1_gamemode.name if self.hated_1v1_gamemode is not None else None}\n'
        info += f'- **Hated 2v2 Gamemode:** {self.hated_2v2_gamemode.name if self.hated_2v2_gamemode is not None else None}\n'
        info += f'- **Hated 4v4 Gamemode:** {self.hated_4v4_gamemode.name if self.hated_4v4_gamemode is not None else None}'
        return info
    

    def has_gamemode_referenced(self, gamemode: Gamemode) -> bool:
        """Return whether the player has referenced a gamemode as one of their favourite/most hated gamemodes."""
        match gamemode.size:
            case 1:
                referenced = True if gamemode.id == self._fav_1v1_gamemode_id or gamemode.id == self._hated_1v1_gamemode_id else False
                return referenced
            case 2:
                referenced = True if gamemode.id == self._fav_2v2_gamemode_id or gamemode.id == self._hated_2v2_gamemode_id else False
                return referenced
            case 4:
                referenced = True if gamemode.id == self._fav_4v4_gamemode_id or gamemode.id == self._hated_4v4_gamemode_id else False
                return referenced
            case _:
                return False


    async def get_profile_embed(self, client: discord.Client, page: int = 0) -> discord.Embed:
        """
        Return:
        - A discord Embed containing the profile page for the `page` value provided.
        - The `page` value, which could be modified if the provided one was invalid.
        """
        # Ensure "page" value is valid  
        min_value, max_value = 0, 1     # NOTE manually handling page number for now...
        if page < min_value:
            page = max_value            # The next of the last is the first
        if page > max_value:
            page = min_value            # The previous of the first is the last

        # Set shared data among profile pages
        embed = discord.Embed(title=self.amq_name, color=discord.Colour.green())
        embed.set_footer(text=f'Page {page+1} / {max_value+1}')
        embed_user = await client.fetch_user(self.discord_id)
        embed_url = 'https://animemusicquiz.com'
        embed_icon_url = 'https://animemusicquiz.com/favicon-32x32.png'

        # Set page specific embed data
        match page:
            case 0:
                embed_name = 'Profile'
                embed.add_field(name='Discord', value=embed_user.display_name, inline=False)
                embed.add_field(name='Rank', value=self.rank.name, inline=False)
                embed.add_field(name='Elo', value='To Be Determined', inline=False)
                embed.set_thumbnail(url=embed_user.display_avatar.url)

            case 1:
                embed_name = 'About me'
                
                fav_1v1 = self.fav_1v1_gamemode.name if self.fav_1v1_gamemode is not None else 'TBD'
                fav_2v2 = self.fav_2v2_gamemode.name if self.fav_2v2_gamemode is not None else 'TBD'
                fav_4v4 = self.fav_4v4_gamemode.name if self.fav_4v4_gamemode is not None else 'TBD'
                hated_1v1 = self.hated_1v1_gamemode.name if self.hated_1v1_gamemode is not None else 'TBD'
                hated_2v2 = self.hated_2v2_gamemode.name if self.hated_2v2_gamemode is not None else 'TBD'
                hated_4v4 = self.hated_4v4_gamemode.name if self.hated_4v4_gamemode is not None else 'TBD'

                embed.add_field(name='😍 1v1', value=fav_1v1, inline=True)
                embed.add_field(name='😍 2v2', value=fav_2v2, inline=True)
                embed.add_field(name='😍 4v4', value=fav_4v4, inline=True)
                embed.add_field(name='💀 1v1', value=hated_1v1, inline=True)
                embed.add_field(name='💀 2v2', value=hated_2v2, inline=True)
                embed.add_field(name='💀 4v4', value=hated_4v4, inline=True)

            case _:
                # should never be reached
                raise ValueError('Invalid page number!')

        embed.set_author(name=embed_name, url=embed_url, icon_url=embed_icon_url)
        return embed, page


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
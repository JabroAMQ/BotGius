import discord

# NOTE With current content it could be a NamedTuple instead of a regular class
# We keep it as a regular class in case additional funcionality is required in the future
class MyEmoji:
    """Class that instantiates an Emoji object combining database data and its real Discord counterpart."""

    def __init__(self, emoji_id: int, emoji_name: str, host_id: int | None, is_join: bool, is_leave: bool, is_poll: bool, discord_obj: discord.Emoji) -> None:
        """Constructor of the MyEmoji class."""
        self._emoji_id = emoji_id
        self._emoji_name = emoji_name
        self._host_id = host_id
        self._is_join = is_join
        self._is_leave = is_leave
        self._is_poll = is_poll
        self._discord_obj = discord_obj

    @property
    def emoji_id(self) -> int:
        return self._emoji_id
    
    @property
    def emoji_name(self) -> str:
        return self._emoji_name

    @property
    def host_id(self) -> int | None:
        return self._host_id

    @property
    def is_join(self) -> bool:
        return self._is_join

    @property
    def is_leave(self) -> bool:
        return self._is_leave
    
    @property
    def is_poll(self) -> bool:
        return self._is_poll

    @property
    def discord_obj(self) -> discord.Emoji:
        return self._discord_obj
import os
import random

from Code.Utilities.read_yaml import load_yaml_content

class Emojis:
    """
    Class that handle everything role related.\n
    The emojis are considered as raw strings (not `discord.Emoji`).
    """    
    _instance = None
    def __new__(cls):
        """Override the __new__ method to return the existing instance of the class if it exists or create a new instance if it doesn't exist yet."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance

    def _set_data(self) -> None:
        """Method that retrieves the emojis ids from its yaml file."""
        yaml_route = os.path.join('Config', 'emojis.yaml')
        emojis_data = load_yaml_content(yaml_route=yaml_route)

        # NOTE default_tour_emojis: Just 2 emojis, join and leave
        # 'join': <default_join_emoji_str>
        # 'leave:' <default_join_emoji_str>
        self.default_tour_emojis: dict[str, str] = emojis_data['default']

        # NOTE custom_tour_emojis: 2 emojis per host, join and leave
        # <host_id_1>:
        #   'join': <custom_join_emoji_str_1>
        #   'leave': <custom_join_moji_str_1>
        # <host_id_2>:
        #   ...
        self.custom_tour_emojis: dict[int, dict[str, str]] = emojis_data['custom']

        # NOTE poll_emojis:
        # <poll_emoji_name_1>: <poll_emoji_str_1>
        # <poll_emoji_name_2>: <poll_emoji_str_2>
        # ...
        self.poll_emojis: dict[str, str] = emojis_data['poll']

        # NOTE other_emojis: emojis that doesn't fit anywhere else
        # <other_emoji_1>: <other_emoji_str_1>
        self.other_emojis: dict[str, str] = emojis_data['others']


    def get_tour_emojis(self, host_id: int) -> tuple[str, str]:
        """
        Return a tuple with 2 emojis (join emoji and leave emoji as raw strings).\n
        These emojis are the custom emojis of the hosts (identified by `host_id`) if exist, otherwise the default ones.
        """
        if host_id not in self.custom_tour_emojis:
            return self.default_tour_emojis['join'], self.default_tour_emojis['leave']
        
        custom_emojis = self.custom_tour_emojis[host_id]
        return custom_emojis['join'], custom_emojis['leave']
    

    def get_poll_emojis(self, n: int = -1) -> list[str]:
        """Return a list with `n` poll emojis. If `n < 1` then it returns a list with all the emojis."""
        # Get all the poll emojis
        reactions: list[str] = list(self.poll_emojis.values())
        
        # Return all the poll emojis if asked for
        if n < 1 or n > len(reactions):
            return reactions
        
        # We randomply pop emojis from the list while we have more emojis than the number asked for
        while len(reactions) > n:
            reaction = random.choice(reactions)
            reactions.remove(reaction)

        return reactions
    

    def get_other_emoji(self, emoji_key: str) -> str:
        """Return an emoji (raw string) given its name (key in the yaml file) or an empty string if it couldn't be found."""
        return self.other_emojis.get(emoji_key, '')
import discord

class Scheduled_Tour:
    """Class representing a scheduled tour."""
    
    def __init__(self, id: int, description: str, host: str, starts_at_timestamp: int, created_at_timestamp: int, updated_at_timestamp) -> None:
        """
        Parameters:
        -----------
        id: `int`
            The database ID of the scheduled tour.
        description: `str`
            The description of the tour.
        host: `str`
            The host of the tour.
        starts_at_timestamp: `int`
            The UNIX timestamp.
        created_at_timestamp: `int`
            The UNIX timestamp of when the scheduled tour was created.
        updated_at_timestamp: `int | None`
            The UNIX timestamp of when the scheduled tour was last updated, or None if it was never updated.

        Raises:
        -------
        `ValueError`:
            If the timestamp string is not in the correct format.
        """
        self.id = id
        self.tour_host = host
        self.tour_description = description
        self.starts_at_timestamp = starts_at_timestamp
        self._created_at_timestamp = created_at_timestamp
        self._updated_at_timestamp = updated_at_timestamp


    def convert_to_discord_timestamp(self) -> str:
        """Convert the UNIX timestamp to a Discord formatted timestamp."""
        return f'<t:{self.starts_at_timestamp}:F>'
    
    def get_log_data(self) -> str:
        """Return a str containing the log data of the scheduled tour."""
        log_data = f'- Host: {self.tour_host}\n'
        log_data += f'- Description: {self.tour_description}\n'
        log_data += f'- Scheduled Time: {self.convert_to_discord_timestamp()}'
        return log_data


    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Scheduled_Tour):
            return NotImplemented
        return self.id == value.id
    
    def __lt__(self, value: object) -> bool:
        if not isinstance(value, Scheduled_Tour):
            return NotImplemented
        return self.starts_at_timestamp < value.starts_at_timestamp

    def __str__(self) -> str:
        return f'{self.tour_host}\'s tour: {self.tour_description}'

    def __repr__(self) -> str:
        now_timestamp = int(discord.utils.utcnow().timestamp())
        if self._updated_at_timestamp and now_timestamp - self._updated_at_timestamp < 86400:   # 1 day = 86400 seconds
            return f'- ⚙️ {self.convert_to_discord_timestamp()} {self.tour_description}, hosted by {self.tour_host}'

        elif now_timestamp - self._created_at_timestamp < 86400:                                # 1 day = 86400 seconds
            return f'- 🆕 {self.convert_to_discord_timestamp()} {self.tour_description}, hosted by {self.tour_host}'
        
        else:
            return f'- {self.convert_to_discord_timestamp()} {self.tour_description}, hosted by {self.tour_host}'
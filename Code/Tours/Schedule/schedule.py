class Scheduled_Tour:
    """Class representing a scheduled tour."""
    
    def __init__(self, id: int, description: str, timestamp: int, host: str) -> None:
        """
        Parameters:
        -----------
        id: `int`
            The database ID of the scheduled tour.
        description: `str`
            The description of the tour.
        timestamp: `int`
            The UNIX timestamp.
        host: `str`
            The host of the tour.

        Raises:
        -------
        `ValueError`:
            If the timestamp string is not in the correct format.
        """
        self.id = id
        self.tour_host = host
        self.tour_description = description
        self.tour_timestamp = timestamp


    def convert_to_discord_timestamp(self) -> str:
        """Convert the UNIX timestamp to a Discord formatted timestamp."""
        return f'<t:{self.tour_timestamp}:F>'
    
    def get_log_data(self) -> str:
        log_data = f'- Host: {self.tour_host}\n'
        log_data += f'- Description: {self.tour_description}\n'
        log_data += f'- Scheduled Time: {self.convert_to_discord_timestamp()}'
        return log_data


    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Scheduled_Tour):
            return NotImplemented
        return self.tour_timestamp == value.tour_timestamp  # Not ideal as two tours can be at the same time but it will be irrelevant for our use case
    
    def __lt__(self, value: object) -> bool:
        if not isinstance(value, Scheduled_Tour):
            return NotImplemented
        return self.tour_timestamp < value.tour_timestamp

    def __str__(self):
        return f'{self.tour_host}\'s tour: {self.tour_description}'

    def __repr__(self):
        return f'- {self.convert_to_discord_timestamp()} {self.tour_description}, hosted by {self.tour_host}'
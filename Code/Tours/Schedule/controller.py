import discord

from Code.Tours.Schedule.database import Scheduled_Tours_Database
from Code.Tours.Schedule.schedule import Scheduled_Tour
from Code.Others.channels import Channels
from Code.Utilities.error_handler import print_exception

class Scheduled_Tour_Controller:
    """Controller to encapsule the Tour Scheduling Logic from the rest of the application."""
    _instance = None
    def __new__(cls):
        """Override the __new__ method to return the existing instance of the class if it exists or create a new instance if it doesn't exist yet.\n"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance
    
    def _set_data(self) -> None:
        """Retrieve all the Scheduled_Tours from the database and store them in a list."""
        self.scheduled_tours: dict[int, Scheduled_Tour] = {}

        for record in Scheduled_Tours_Database.get_all_scheduled_tours():
            id, guild_id, description, host, starts_at, created_at, updated_at = record
            scheduled_tour = Scheduled_Tour(id, guild_id, description, host, starts_at, created_at, updated_at)
            self.scheduled_tours[id] = scheduled_tour

    
    def add_scheduled_tour(self, guild_id: int, description: str, host: str, timestamp: int) -> tuple[bool, str]:
        """
        Create a new Scheduled_Tour and add it into the database and the catalog.
        
        Returns a tuple where the first element is a bool indicating if the operation was successful and the second element is the log data of the created Scheduled_Tour
        """
        try:
            created_at = int(discord.utils.utcnow().timestamp())
            id = Scheduled_Tours_Database.add_scheduled_tour(guild_id, description, host, timestamp, created_at)
            new_scheduled_tour = Scheduled_Tour(id, guild_id, description, host, timestamp, created_at, None)
            self.scheduled_tours[id] = new_scheduled_tour
            return True, new_scheduled_tour.get_log_data()

        except Exception as error:
            print_exception(error)
            return False, ''
    

    def delete_scheduled_tour(self, tour_id: int) -> tuple[bool, str]:
        """
        Delete a Scheduled_Tour from the database and the catalog.
        
        Returns a tuple where the first element is a bool indicating if the operation was successful and the second element is the log data of the deleted Scheduled_Tour
        """
        try:
            log_data = self.scheduled_tours[tour_id].get_log_data()
            Scheduled_Tours_Database.delete_scheduled_tour(tour_id)
            del self.scheduled_tours[tour_id]
            return True, log_data
        
        except Exception as error:
            print_exception(error)
            return False, ''
        
    
    def edit_scheduled_tour(self, tour_id: int, description: str = None, host: str = None, timestamp: int = None) -> tuple[bool, str]:
        """
        Delete a Scheduled_Tour in the database and in the catalog.

        Returns a tuple where the first element is a bool indicating if the operation was successful and the second element is the log data of the edited Scheduled_Tour
        """
        try:
            tour = self.scheduled_tours[tour_id]

            # Log purposes
            old_description = tour.tour_description
            old_host = tour.tour_host
            old_timestamp = tour.convert_to_discord_timestamp()

            # Get new values
            new_description = description or tour.tour_description
            new_host = host or tour.tour_host
            new_timestamp = timestamp or tour.starts_at_timestamp
            new_updated_at = int(discord.utils.utcnow().timestamp())
            
            # Apply the changes
            Scheduled_Tours_Database.edit_scheduled_tour(tour_id, new_description, new_host, new_timestamp, new_updated_at)
            tour.tour_description = new_description
            tour.tour_host = new_host
            tour.starts_at_timestamp = new_timestamp
            tour._updated_at_timestamp = new_updated_at
            
            log_data = ''
            if old_host:
                log_data += f'- Host: {old_host} -> {tour.tour_host}\n'
            if old_description:
                log_data += f'- Description: {old_description} -> {tour.tour_description}\n'
            if old_timestamp:
                log_data += f'- Scheduled Time: {old_timestamp} -> {tour.convert_to_discord_timestamp()}\n'

            return True, log_data

        except Exception as error:
            print_exception(error)
            return False, ''


    def represent_all_scheduled_tours(self, guild_id: int) -> str:
        """Return a str representation of all the Scheduled_Tours in the catalog for a specific guild."""
        guild_scheduled_tours = [scheduled_tour for scheduled_tour in sorted(self.scheduled_tours.values()) if scheduled_tour.guild_id == guild_id]

        representation = '**Upcoming Scheduled Tours**:\n\n'        
        for i, tour in enumerate(guild_scheduled_tours, start=1):
            representation += f'{i}. {repr(tour)}\n'
        representation += f'\nLast updated: <t:{int(discord.utils.utcnow().timestamp())}:R>'
        
        return representation
    
    def get_tour_from_fixed_id(self, guild_id: int, fixed_id: int) -> tuple[bool, Scheduled_Tour | None]:
        """
        The scheduled tour message looks like this:
            1. [optional_emoji]"timestamp_1" "description_1", "host_1"
            2. [optional_emoji]"timestamp_2" "description_2", "host_2"
            3. [optional_emoji]"timestamp_3" "description_3", "host_3"
            ...

        `fixed_id` is that first character(s) from each line (1, 2, 3...).\n
        Return a tuple[bool, Scheduled_Tour] containing whether the tour was found and the tour itself (if found only)
        """
        guild_scheduled_tours = [scheduled_tour for scheduled_tour in sorted(self.scheduled_tours.values()) if scheduled_tour.guild_id == guild_id]
        index = fixed_id - 1

        if 0 <= index < len(guild_scheduled_tours):
            tour = guild_scheduled_tours[index]
            return True, tour
        
        return False, None
    

    async def allow_additions(self, interaction: discord.Interaction) -> bool:
        """
        Return whether we are already close enough to discord's message length limit cap in the server determined by `interaction` parameter.
        - NOTE For now we don't let scheduling more tours if the message length is already close enough to discord message limit (2000 characters)
        - NOTE Hard capping at 1950 character length for now to save some space for other tours's edition (additional description information is added)
        - TODO Create a second message if reaching the length limit and reorder the scheduled tours?
        """
        MAX_ALLOWED_LENGTH = 1950
        scheduled_tours_message = await Channels().get_tour_announcements_message(interaction.client, interaction.guild_id)
        return len(scheduled_tours_message.content) < MAX_ALLOWED_LENGTH
    
    async def allow_modifications(self, interaction: discord.Interaction, fixed_id: int, description: str = None, timestamp: int = None, host: str = None) -> bool:
        """
        Return whether the modifications exceed discord's message length limit cap in the server determined by `interaction` parameter.
        - TODO Create a second message if reaching the length limit and reorder the scheduled tours?
        """
        MAX_ALLOWED_LENGTH = 2000

        # Get the message's length
        scheduled_tours_message = await Channels().get_tour_announcements_message(interaction.client, interaction.guild_id)
        message_content = scheduled_tours_message.content

        # Get the specific tour representation length
        exists, tour = self.get_tour_from_fixed_id(interaction.guild_id, fixed_id)
        if not exists:
            return False
        
        # Get the hypothetical new values
        new_desc = description or tour.tour_description
        new_host = host or tour.tour_host
        new_time = timestamp or tour.starts_at_timestamp
        new_line_content = f" ⚙️ <t:{new_time}:F> {new_desc}, hosted by {new_host}"

        # Replace the old line content by the new one
        lines = message_content.split('\n')
        target_prefix = f"{fixed_id}."
        for index, line in enumerate(lines):
            if line.strip().startswith(target_prefix):
                lines[index] = f"{target_prefix}{new_line_content}"
                break

        # Check if the hypothetical new representation is longer than the MAX_ALLOWED_LENGTH
        new_message = '\n'.join(lines)
        return len(new_message) <= MAX_ALLOWED_LENGTH
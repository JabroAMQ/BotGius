import discord

from Code.Tours.Schedule.database import Scheduled_Tours_Database
from Code.Tours.Schedule.schedule import Scheduled_Tour
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
            old_description, old_host, old_timestamp = None, None, None
            if description:
                old_description = tour.tour_description
            if host:
                old_host = tour.tour_host
            if timestamp:
                old_timestamp = tour.starts_at_timestamp

            new_description = description if description else tour.tour_description
            new_host = host if host else tour.tour_host
            new_timestamp = timestamp if timestamp else tour.starts_at_timestamp
            new_updated_at = int(discord.utils.utcnow().timestamp())
            
            Scheduled_Tours_Database.edit_scheduled_tour(tour_id, new_description, new_host, new_timestamp, new_updated_at)
            tour.tour_description = new_description
            tour.tour_host = new_host
            tour.starts_at_timestamp = new_timestamp
            tour._updated_at_timestamp = new_updated_at
            
            log_data = ''
            if old_host:
                log_data += f'- Host: {old_host} -> {new_host}\n'
            if old_description:
                log_data += f'- Description: {old_description} -> {new_description}\n'
            if old_timestamp:
                log_data += f'- Scheduled Time: {old_timestamp} -> {new_timestamp}\n'

            return True, log_data

        except Exception as error:
            print_exception(error)
            return False, ''
        
    def count_scheduled_tours(self, guild_id: int) -> int:
        """Return the number of Scheduled_Tours stored in the catalog for a specific guild."""
        return sum(1 for tour in self.scheduled_tours.values() if tour.guild_id == guild_id)
    
    def get_all_scheduled_tours(self, guild_id: int) -> list[tuple[str, int]]:
        """Return a list of tuples containing all the Scheduled_Tours representation, and its id, stored in the catalog for a specific guild."""
        return [(str(tour), tour.id) for tour in sorted(self.scheduled_tours.values()) if tour.guild_id == guild_id]


    def represent_all_scheduled_tours(self, guild_id: int) -> str:
        """Return a str representation of all the Scheduled_Tours in the catalog for a specific guild."""
        guild_scheduled_tours = [scheduled_tour for scheduled_tour in sorted(self.scheduled_tours.values()) if scheduled_tour.guild_id == guild_id]

        representation = '**Upcoming Scheduled Tours**:\n\n'        
        for tour in guild_scheduled_tours:
            representation += repr(tour) + '\n'
        representation += f'\nLast updated: <t:{int(discord.utils.utcnow().timestamp())}:R>'
        
        return representation
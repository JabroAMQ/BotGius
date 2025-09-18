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
            id, description, timestamp, host = record
            scheduled_tour = Scheduled_Tour(id, description, timestamp, host)
            self.scheduled_tours[id] = scheduled_tour

    
    def add_scheduled_tour(self, description: str, timestamp: str, host: str) -> tuple[bool, str]:
        """
        Create a new Scheduled_Tour and add it into the database and the catalog.
        
        Returns a tuple where the first element is a bool indicating if the operation was successful and the second element is the log data of the created Scheduled_Tour
        """
        try:
            id = Scheduled_Tours_Database.add_scheduled_tour(description, timestamp, host)
            new_scheduled_tour = Scheduled_Tour(id, description, timestamp, host)
            self.scheduled_tours[id] = new_scheduled_tour
            return True, new_scheduled_tour.get_log_data()

        except Exception as error:
            print_exception(error)
            return False, ''
    

    def delete_scheduled_tour(self, scheduled_tour_id: int) -> tuple[bool, str]:
        """
        Delete a Scheduled_Tour from the database and the catalog.
        
        Returns a tuple where the first element is a bool indicating if the operation was successful and the second element is the log data of the deleted Scheduled_Tour
        """
        try:
            log_data = self.scheduled_tours[scheduled_tour_id].get_log_data()
            Scheduled_Tours_Database.delete_scheduled_tour(scheduled_tour_id)
            del self.scheduled_tours[scheduled_tour_id]
            return True, log_data
        
        except Exception as error:
            print_exception(error)
            return False, ''
        
    def count_scheduled_tours(self) -> int:
        """Return the number of Scheduled_Tours stored in the catalog."""
        return len(self.scheduled_tours)
    
    def get_all_scheduled_tours(self) -> list[tuple[str, int]]:
        """Return a list of tuples containing all the Scheduled_Tours representation, and its id, stored in the catalog."""
        return [(str(tour), tour.id) for tour in sorted(self.scheduled_tours.values())]


    def represent_all_scheduled_tours(self) -> str:
        """Return a str representation of all the Scheduled_Tours in the catalog."""
        representation = '**Upcoming Scheduled Tours**:\n\n'
        
        for tour in sorted(self.scheduled_tours.values()):
            representation += repr(tour) + '\n'

        return representation.strip()
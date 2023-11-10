import discord

from Code.Tours.tour import Tour

class Tours_Controller:
    """Controller to encapsule the Tours Logic from the rest of the application."""
    # NOTE this class is more like a catalog rather than a controller.
    # The tour is created and stored here but the tour logic is called directly from the interactions

    _instance = None
    def __new__(cls) -> None:
        """Override the __new__ method to return the existing instance of the class if it exists or create a new instance if it doesn't exist yet.\n"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance
    
    def _set_data(self) -> None:
        """Creates the active tours catalog."""
        self.tours_active = {}


    def start_new_tour(
        self,
        host : discord.User,
        guild : discord.Guild,
        timer : int = None,
        size : int = None,
        elo : bool = False,
        info : str = ''
    ) -> Tour:
        """Starts a new tour. Returns the tour created."""
        # TODO Tour ID
        tour_id = 0

        tour = Tour(tour_id=tour_id, host=host, guild=guild, timer=timer, max_players_size=size, counts_for_elo=elo, tour_info=info)
        self.tours_active[tour_id] = tour
        return tour
    

    def get_current_tour(self) -> Tour | None:
        """Returns the tour that is currently active."""
        # TODO Tour ID
        tour_id = 0
        return self.tours_active.get(tour_id)
    

    async def end_current_tour(self, client : discord.Client) -> None:
        """Ends the tour that is currently active."""
        # TODO Tour ID
        tour_id = 0
        tour : Tour = self.tours_active.get(tour_id)
        
        # Remove the roles from the players
        [await team.reset_roles(client) for team in tour.teams]
        
        # Prevent people for joining the ended tour
        tour.is_tour_active = False
        tour.is_tour_open = False

        del self.tours_active[tour_id]
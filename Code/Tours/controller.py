import discord

from Code.Tours.tour import Tour
from Code.Others.roles import Roles
from Code.Utilities.error_handler import error_handler_decorator

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
        self._tour_cont = 0
        self.tours: dict[int, Tour] = {}


    def start_new_tour(
        self,
        host: discord.User,
        guild: discord.Guild,
        timer: int = None,
        size: int = None,
        elo: bool = False,
        info: str = ''
    ) -> Tour:
        """
        Starts a new tour, associates to it a `tour_id` and store it in the `tours` dict.\n
        Returns the tour created.
        """
        tour_id = self._tour_cont
        self._tour_cont += 1

        tour = Tour(tour_id=tour_id, host=host, guild=guild, timer=timer, max_players_size=size, counts_for_elo=elo, tour_info=info)
        self.tours[tour_id] = tour
        return tour
    

    async def get_current_tour(self, interaction: discord.Interaction) -> Tour | None:
        """Returns the tour that is currently active."""

        class Tours_Dropdown(discord.ui.Select):
        
            def __init__(self, active_tours: list[Tour]):
                options = [
                    discord.SelectOption(label=f'{tour.host.name}\'s Tour: "{tour.tour_info[:20]}"', value=str(i))
                    for i, tour in enumerate(active_tours)
                ]
                super().__init__(placeholder='Select a tour to apply the changes', options=options)
                self.active_tours = active_tours
                self.selected_tour: Tour | None = None

            @error_handler_decorator()
            async def callback(self, new_interaction: discord.Interaction):
                await new_interaction.response.defer(ephemeral=True)
                self.selected_tour = self.active_tours[int(self.values[0])]
                self.view.stop()
                await new_interaction.followup.send(content='Tour successfully selected', ephemeral=True)
    

        class Tours_Dropdown_View(discord.ui.View):
            
            def __init__(self, active_tours: list[Tour]):
                super().__init__(timeout=180)
                self.dropdown = Tours_Dropdown(active_tours)
                self.add_item(self.dropdown)

            async def on_timeout(self):
                self.stop()
            

        active_tours = [tour for tour in self.tours.values() if tour.is_tour_active]
        if not active_tours:
            return None
        
        if len(active_tours) == 1:
            return active_tours[0]

        view = Tours_Dropdown_View(active_tours)
        await interaction.followup.send(view=view, ephemeral=True)
        await view.wait()
        return view.dropdown.selected_tour
    

    async def end_current_tour(self, tour: Tour, guild: discord.Guild) -> None:
        """Ends the tour that is currently active."""
        # Remove the drafter roles from the players
        [await Roles().remove_drafter_role(guild, player.discord_id) for player in tour.players]

        # Remove the roles from the players
        [await team.reset_roles(guild) for team in tour.teams]
        
        # Prevent people for joining the ended tour
        tour.is_tour_active = False
        tour.is_tour_open = False

        # NOTE we do not remove the ended tour from self.tours dict
        # TODO tours database?
from abc import ABC, abstractmethod

from Commands.utilities import Tour_Helpers

import discord

class Commands(ABC):
    """Commands's Abstract Base Class. All Commands classes must inherit from this one."""

    def __init__(self) -> None:
        """Base Hierarchy Constructor."""
        pass

    def is_user_admin(self, interaction : discord.Interaction) -> bool:
        """Return whether the interaction user is in the admin's list"""
        admins = Tour_Helpers().get_admins()
        return interaction.user.id in admins
    
    def is_user_tour_helper(self, interaction : discord.Interaction) -> bool:
        """Return whether the interaction user is in the tour helper (or admin) lists"""
        admins = Tour_Helpers().get_admins()
        helpers = Tour_Helpers().get_helpers()
        return interaction.user.id in admins or interaction.user.id in helpers
    
    @abstractmethod
    def load_commands(self, client : discord.Client) -> None:
        pass
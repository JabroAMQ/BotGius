import os
import importlib
from copy import copy

import discord

from Code.Utilities.read_yaml import load_yaml_content
from Code.Utilities.error_handler import print_exception
from Code.Gamemodes.controller import Main_Controller
from Code.Tours.controller import Tours_Controller
from Code.Players.controller import Players_Controller
from Code.Players.main_ranking import Ranking
from Code.Others.channels import Channels
from Code.Others.emojis import Emojis
from Code.Others.roles import Roles

def load_app_commands(client : discord.Client):
    """
    Load all the `discord.app_commands` commands found in the `./Commands/Commands` subdirectory dynamically.\n
    Parameters:
    -----------
    - `client` : `discord.Client`
        The Discord Client to load commands into.
    """
    # importing inside function to avoid circular import error
    from Commands.base import Commands

    command_directory_path = os.path.join('Commands', 'Commands')

    for root, _, files in os.walk(command_directory_path):
        files = [file for file in files if file.endswith('.py')]
        
        for file in files:
            module_path = os.path.relpath(os.path.join(root, file))
            module_name = module_path[:-3].replace(os.path.sep, '.')
            
            try:
                module = importlib.import_module(module_name)
                class_name = f'{module_name.split(".")[-1].capitalize()}_Commands'

                if hasattr(module, class_name):
                    command_class = getattr(module, class_name)
                    if issubclass(command_class, Commands):
                        command_class().load_commands(client)
                    else:
                        print(f'Class {class_name} in module {module_name} does not inherit from Commands base class')
                
                else:
                    print(f'Invalid class name ({class_name}) in module {module_name} (check capitalizations in `class_name`)')

            except ImportError as error:
                print(f'Failed to import module {module_name}')
                print_exception(error)


def load_controllers() -> None:
    """Auxiliar function to load the singleton controllers so that delay is not introduced when they are first needed."""
    # Saving the reference is not needed
    Main_Controller()
    Tours_Controller()
    Players_Controller()
    Ranking()
    Channels()
    Emojis()
    Roles()
    Tour_Helpers()


class Tour_Helpers:
    """Singleton class to get the list of tour helpers/admins."""
    _instance = None
    def __new__(cls) -> None:
        """Override the __new__ method to return the existing instance of the class if it exists or create a new instance if it doesn't exist yet.\n"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance
    
    def _set_data(self) -> None:
        """Loads into memory the tour helpers / admins discord ids."""
        hosts_data = load_yaml_content(yaml_route=os.path.join('Config', 'hosts.yaml'))
        self.admins : list[int] = hosts_data['admins']
        self.helpers : list[int] = hosts_data['helpers']

    def get_admins(self) -> list[int]:
        """Return the ids of all the tour's admins."""
        return copy(self.admins)
    
    def get_helpers(self) -> list[int]:
        """Return the ids of all the tour's helpers."""
        return copy(self.helpers)
import os

import discord

from Code.Utilities.read_yaml import load_yaml_content

class Roles:
    """Class that handle everything role related."""
    
    _instance = None
    def __new__(cls):
        """Override the __new__ method to return the existing instance of the class if it exists or create a new instance if it doesn't exist yet.\n"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance

    
    def _set_data(self) -> None:
        """Method that retrieves the roles ids from its yaml file."""
        yaml_route = os.path.join('Config', 'roles.yaml')
        roles_data = load_yaml_content(yaml_route=yaml_route)

        self.main_guild_id: int = roles_data['teams']['main']['id']
        self.test_guild_id: int = roles_data['teams']['test']['id']

        self.main_guild_roles_ids: list[int] = roles_data['teams']['main']['roles']
        self.test_guild_roles_ids: list[int] = roles_data['teams']['test']['roles']

        self.pings: list[str] = [roles_data['pings']['bullies'], roles_data['pings']['capos']]

    
    def _get_team_roles(self, guild: discord.Guild, role_index: int = 0) -> tuple[discord.Role, list[discord.Role]]:
        """
        Given a guild and a role_index, return a tuple formed by 2 elemets:
        - `Role`: The role with index `role_index` among all the team's roles from the guild.
        - `list[Role]`: All the team's roles from the guild except the one with `role_index`.

        Raises:
        -----------
        - ValueError: if the guild id is not valid.
        """
        match guild.id:
            case self.main_guild_id:
                all_roles = [guild.get_role(role_id) for role_id in self.main_guild_roles_ids]
                role = all_roles.pop(role_index)
                return role, all_roles
            
            case self.test_guild_id:
                all_roles = [guild.get_role(role_id) for role_id in self.test_guild_roles_ids]
                role = all_roles.pop(role_index)
                return role, all_roles
            
            case _:
                raise ValueError('Invalid Guild ID')


    def get_ping_roles(self) -> str:
        """Return a string containing the mention of all the ping roles."""        
        return ' '.join(self.pings)
    

    async def remove_team_roles(self, guild: discord.Guild, player_id: int):
        """Remove all team roles from the player (identified by its discord id `player_id`) from the guild (identified by its id `guild_id`)."""
        member = guild.get_member(player_id)
        if member is None:
            # NOTE If raising an exception is prefered, make sure to handle it properly so when using a command like /tour_end or /reset_teams
            # the role removal chain is not broken
            print(f'Invalid User ID ({player_id}). Player not in Guild ({guild.name if isinstance(guild, discord.Guild) else guild})?')
            return
        
        role, other_roles = self._get_team_roles(guild)
        roles = other_roles + [role]
        roles_to_remove = [role for role in roles if role in member.roles]
        
        try:
            await member.remove_roles(*roles_to_remove)
        except Exception as e:
            print(f'Couldn\'t remove role from player {player_id}: {e}')


    async def add_team_role(self, guild: discord.Guild, player_id: int, role_index: int):
        """Add the team role with index `role_index` to the player (identified by its discord id `player_id`) in the guild provided."""
        member = guild.get_member(player_id)
        if member is None:
            # NOTE If raising an exception is prefered, make sure to handle it properly so when using a command like /team_players_add or /team_randomize
            # the loop is not broken
            print(f'Invalid User ID ({player_id}). Player not in Guild ({guild.name if isinstance(guild, discord.Guild) else guild})?')
            return
        
        role, other_roles = self._get_team_roles(guild, role_index)

        try:
            roles_to_remove = [role for role in other_roles if role in member.roles]
            await member.remove_roles(*roles_to_remove)
            await member.add_roles(role)
        except Exception as e:
            print(f'Couldn\'t remove role from player {player_id}: {e}')

    
    async def add_all_team_roles(self, guild: discord.Guild, player_id: int):
        """
        Add all team roles to the player (identified by its discord id `player_id`) in the guild provided.
        
        Raises:
        -----------
        - ValueError: if the player or guild ids are not valid.
        """
        member = guild.get_member(player_id)
        if member is None:
            raise ValueError('Invalid User ID')
        
        role, other_roles = self._get_team_roles(guild)
        roles_to_add = other_roles + [role]

        try:
            await member.add_roles(*roles_to_add)
        except Exception as e:
            print(f'Couldn\'t remove role from player {player_id}: {e}')
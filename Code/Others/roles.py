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

        self.main_guild_id : int = roles_data['teams']['main']['id']
        self.test_guild_id : int = roles_data['teams']['test']['id']

        self.main_guild_roles_ids : list[int] = roles_data['teams']['main']['roles']
        self.test_guild_roles_ids : list[int] = roles_data['teams']['test']['roles']

        self.pings_ids : list[str] = [roles_data['pings']['bullies'], roles_data['pings']['capos']]


    def _get_member_and_guild(self, client : discord.Client, user_id : int, guild_id : int) -> tuple[discord.Member, discord.Guild]:
        """
        Given a user and a guild ids, return a tuple with the discord Member and Guild objects that the ids are related to.

        Raises:
        -----------
        - ValueError: if the user or guild ids are not valid.
        """
        match guild_id:
            case self.main_guild_id:
                guild = client.get_guild(self.main_guild_id)
            case self.test_guild_id:
                guild = client.get_guild(self.test_guild_id)
            case _:
                raise ValueError('Invalid Guild ID')
            
        member = guild.get_member(user_id)
        if not member:
            raise ValueError('Invalid User ID')
        
        return member, guild
    
    def _get_team_roles(self, client : discord.Client, guild_id : int, role_index : int = 0) -> tuple[discord.Role, list[discord.Role]]:
        """
        Given a guild id and a role_index, return a tuple formed by 2 elemets:
        - `Role`: The role with index `role_index` among all the team's roles from the guild with `guild_id` id.
        - `list[Role]`: All the team's roles from the guild with `guild_id` id except the one with `role_index`.

        Raises:
        -----------
        - ValueError: if the guild id is not valid.
        """
        match guild_id:
            case self.main_guild_id:
                guild = client.get_guild(self.main_guild_id)
                all_roles = [guild.get_role(role_id) for role_id in self.main_guild_roles_ids]
                role = all_roles.pop(role_index)
                return role, all_roles
            
            case self.test_guild_id:
                guild = client.get_guild(self.test_guild_id)
                all_roles = [guild.get_role(role_id) for role_id in self.test_guild_roles_ids]
                role = all_roles.pop(role_index)
                return role, all_roles
            
            case _:
                raise ValueError('Invalid Guild ID')


    def get_ping_roles(self, client : discord.Client) -> str:
        """Return a string containing the mention of all the ping roles."""
        guild = client.get_guild(self.main_guild_id)
        
        # NOTE Only needed for test bot as test bot is not in the main guild server which would raise an error as guild = None in that case
        if guild is None:
            return ' '.join(["@deleted-role" for _ in self.pings_ids])
        
        return ' '.join([guild.get_role(role_id) for role_id in self.pings_ids])
    

    async def remove_team_roles(self, client : discord.Client, player_id : int, guild_id : int):
        """
        Remove all team roles from the player (identified by its discord id `player_id`) from the guild (identified by its id `guild_id`).
        
        Raises:
        -----------
        - ValueError: if the player or guild ids are not valid.
        """
        member, _ = self._get_member_and_guild(client, player_id, guild_id)
        role, other_roles = self._get_team_roles(client, guild_id)
        roles = other_roles + [role]
        roles_to_remove = [role for role in roles if role in member.roles]
        
        try:
            await member.remove_roles(*roles_to_remove)
        except Exception:
            print(f'Couldn\'t remove role from player {player_id}')


    async def add_team_role(self, client : discord.Client, player_id : int, guild_id : int, role_index : int):
        """
        Add the team role with index `role_index` to the player (identified by its discord id `player_id`) in the guild (identified by its id `guild_id`).
        
        Raises:
        -----------
        - ValueError: if the player or guild ids are not valid.
        """
        member, _ = self._get_member_and_guild(client, player_id, guild_id)
        role, other_roles = self._get_team_roles(client, guild_id, role_index)

        try:
            roles_to_remove = [role for role in other_roles if role in member.roles]
            await member.remove_roles(*roles_to_remove)
            await member.add_roles(role)
        except Exception:
            print(f'Couldn\'t add role to player {player_id}')

    
    async def add_all_team_roles(self, client : discord.Client, player_id : int, guild_id : int):
        """
        Add all team roles to the player (identified by its discord id `player_id`) in the guild (identified by its id `guild_id`).
        
        Raises:
        -----------
        - ValueError: if the player or guild ids are not valid.
        """
        member, _ = self._get_member_and_guild(client, player_id, guild_id)
        role, other_roles = self._get_team_roles(client, guild_id)
        roles_to_add = other_roles + [role]

        try:
            await member.add_roles(*roles_to_add)
        except Exception:
            print(f'Couldn\'t add role to player {player_id}')
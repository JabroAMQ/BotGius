import random

import discord

from Code.Others.Emojis.database import Emojis_Database
from Code.Others.Emojis.emoji import MyEmoji
from Code.Utilities.error_handler import print_exception

class Emojis_Controller:
    """Controller to encapsule the Emojis Logic from the rest of the application."""
    _instance = None
    def __new__(cls) -> 'Emojis_Controller':
        """Override the __new__ method to return the existing instance of the class if it exists or create a new instance if it doesn't exist yet.\n"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance
    
    def _set_data(self) -> None:
        """Retrieve all the Emojis from the Database and load them into memory."""
        self._emojis_by_ids: dict[int, MyEmoji] = {}
        self._emojis_by_names: dict[str, MyEmoji] = {}

        self._DEFAULT_JOIN_EMOJI_NAME = 'yoaichi'
        self._DEFAULT_LEAVE_EMOJI_NAME = 'yonoaichi'
        self._DEFAULT_EXTRA_EMOJI_NAME = '20espiando'

    async def initialize(self, bot: discord.Client) -> None:
        """Fetches DB entries and Discord API data emojis."""
        self._emojis_by_ids.clear()
        
        try:
            db_emojis = Emojis_Database.get_all_emojis()
            discord_emojis = await bot.fetch_application_emojis()
            discord_emojis_dict = {e.id: e for e in discord_emojis}

            for emoji_id, emoji_name, host_id, is_join, is_leave, is_poll in db_emojis:
                if emoji_id not in discord_emojis_dict:
                    print(f'{emoji_id} ({emoji_name}) is in the Database but not uploaded as an application emoji in Discord. Skipping it...')
                    continue
                
                my_emoji = MyEmoji(
                    emoji_id=emoji_id, 
                    emoji_name=emoji_name, 
                    host_id=host_id, 
                    is_join=is_join, 
                    is_leave=is_leave,
                    is_poll=is_poll,
                    discord_obj=discord_emojis_dict[emoji_id]
                )
                
                self._emojis_by_ids[emoji_id] = my_emoji
                self._emojis_by_names[emoji_name] = my_emoji
                               
        except discord.HTTPException as e:
            print(f'Error while trying to connect to Discord\'s API during emoji initialization: {e}')
        except Exception as e:
            print(f'Unexpected error during Emojis_Controller initialization: {e}')


    def _get_my_emoji_by_id(self, emoji_id: int) -> MyEmoji | None:
        """Return the discord.Emoji object given its id."""
        return self._emojis_by_ids.get(emoji_id)
    
    def _get_my_emoji_by_name(self, emoji_name: str) -> MyEmoji | None:
        """Return the discord.Emoji object given its name."""
        return self._emojis_by_names.get(emoji_name)

    def get_discord_emoji(self, emoji_data: int | str) -> discord.Emoji | None:
        """Return the discord.Emoji object given its id or name."""
        if type(emoji_data) == int:
            emoji = self._get_my_emoji_by_id(emoji_data)
        elif type(emoji_data) == str:
            emoji = self._get_my_emoji_by_name(emoji_data)
        else:
            raise TypeError('Unsupported Type: The emoji_data must be an integer or string')
        
        return emoji.discord_obj if emoji else None
    

    def get_tour_emojis(self, host_id: int) -> tuple[discord.Emoji, discord.Emoji]:
        """
        Return a tuple with 2 emojis (join and leave emojis).\n
        These emojis are the custom emojis of the hosts (identified by `host_id`) if exist, otherwise the default ones.
        """
        join_my_emoji = next((e for e in self._emojis_by_ids.values() if e.host_id == host_id and e.is_join), None)
        join_discord_emoji = join_my_emoji.discord_obj if join_my_emoji else self.get_discord_emoji(self._DEFAULT_JOIN_EMOJI_NAME)

        leave_my_emoji = next((e for e in self._emojis_by_ids.values() if e.host_id == host_id and e.is_leave), None)
        leave_discord_emoji = leave_my_emoji.discord_obj if leave_my_emoji else self.get_discord_emoji(self._DEFAULT_LEAVE_EMOJI_NAME)

        return join_discord_emoji, leave_discord_emoji
    

    def get_poll_emojis(self, n: int = -1) -> list[discord.Emoji]:
        """Return a list with `n` poll emojis. If `n < 1` then it returns a list with all the poll emojis."""
        poll_emojis = [my_emoji.discord_obj for my_emoji in self._emojis_by_ids.values() if my_emoji.is_poll]        

        if n < 1 or n > len(poll_emojis):
            return poll_emojis
        
        while len(poll_emojis) > n:
            reaction = random.choice(poll_emojis)
            poll_emojis.remove(reaction)

        return poll_emojis
    

    def get_extra_emoji(self) -> discord.Emoji:
        """Return `20espiando` emoji."""
        return self.get_discord_emoji(self._DEFAULT_EXTRA_EMOJI_NAME)
    

    def _get_host_emoji(self, host_id: int, is_join: bool) -> MyEmoji | None:
        """Helper to find an existing custom emoji for a specific host and state."""
        for emoji in self._emojis_by_ids.values():
            if emoji.host_id == host_id and emoji.is_join == is_join and emoji.is_leave == (not is_join):
                return emoji
        return None

    async def _delete_emoji_instance(self, emoji: MyEmoji) -> None:
        """Private core method to delete an emoji from Discord API, Database, and Catalogs at once."""
        await emoji.discord_obj.delete()        
        Emojis_Database.delete_custom_emoji(emoji.emoji_id)
        
        if emoji.emoji_id in self._emojis_by_ids:
            del self._emojis_by_ids[emoji.emoji_id]

        if emoji.emoji_name in self._emojis_by_names:
            del self._emojis_by_names[emoji.emoji_name]
    

    async def add_emoji(self, interaction: discord.Interaction, attachment: discord.Attachment, is_join: bool) -> bool:
        """
        Manages the complete lifecycle of a host's custom emoji.
        Deletes the old one (if it exists) from Discord, memory, and DB, then uploads and registers the new one.
        """
        user_id = interaction.user.id
        suffix = 'join' if is_join else 'leave'
        target_name = f'{user_id}_{suffix}'

        try:
            # Check if a custom emoji already exists for the particular case
            existing_emoji = self._get_host_emoji(user_id, is_join)
            if existing_emoji:
                await self._delete_emoji_instance(existing_emoji)

            # Download emoji image
            image_bytes = await attachment.read()
        
            # Add the emoji to Discord, the Database and the Catalogs
            api_emoji = await interaction.client.create_application_emoji(name=target_name, image=image_bytes)
            
            new_my_emoji = MyEmoji(
                emoji_id=api_emoji.id,
                emoji_name=api_emoji.name,
                host_id=user_id,
                is_join=is_join,
                is_leave=not is_join,
                is_poll=False,
                discord_obj=api_emoji
            )

            self._emojis_by_ids[new_my_emoji.emoji_id] = new_my_emoji
            self._emojis_by_names[new_my_emoji.emoji_name] = new_my_emoji

            Emojis_Database.add_custom_emoji(
                new_my_emoji.emoji_id, 
                new_my_emoji.emoji_name, 
                new_my_emoji.host_id, 
                new_my_emoji.is_join
            )
            
            return True

        except Exception as e:
            print_exception(e)
            return False
        

    async def delete_emoji(self, interaction: discord.Interaction, is_join: bool) -> tuple[bool, bool]:
        """
        Deletes a host's custom emoji from Discord, Database, and Catalogs (if it exists).
        
        Returns a tuple with 2 `bool` values meaning:
            1. Whether a custom emoji could be found given the provided parameters.
            2. Whether there was an error while trying to delete the existing emoji.
        """
        existing_emoji = self._get_host_emoji(interaction.user.id, is_join)  
        if not existing_emoji:
            # No emoji to delete
            return False, False

        try:          
            await self._delete_emoji_instance(existing_emoji)
            # Emoji found and deleted successfully
            return True, True
                    
        except Exception as e:
            print_exception(e)
            # Emoji could be found, but there was an error while deleting it
            return True, False
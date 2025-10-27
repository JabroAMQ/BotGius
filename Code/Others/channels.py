import os

import discord

from Code.Utilities.read_yaml import load_yaml_content

class Channels:
    """Class that handle everything channel related."""
    
    _instance = None
    def __new__(cls):
        """Override the __new__ method to return the existing instance of the class if it exists or create a new instance if it doesn't exist yet.\n"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance

    def _set_data(self) -> None:
        """Method that retrieves the channels ids from its yaml file."""
        yaml_route = os.path.join('Config', 'channels.yaml')
        channels_data = load_yaml_content(yaml_route=yaml_route)

        self.main_guild_id = channels_data['main']['guild']
        self.test_guild_id = channels_data['test']['guild']
        self.new_guild_id = channels_data['new_server']['guild']                # NOTE delete when moved

        self.host_channel_id = channels_data['main']['host_chat']
        self.new_host_channel_id = channels_data['new_server']['host_chat']     # NOTE delete when moved
        self.feedback_channel_id = channels_data['test']['feedback']
        self.report_channel_id = channels_data['test']['report']
        self.picks_channel_id = channels_data['test']['picks']

        self.tour_announcements_channel_id = channels_data['new_server']['tour_announcements']['channel']           # NOTE change to main when moved
        self.tour_announcements_message_id = channels_data['new_server']['tour_announcements']['message']           # NOTE change to main when moved
        self.test_tour_announcements_channel_id = channels_data['test']['tour_announcements']['channel']
        self.test_tour_announcements_message_id = channels_data['test']['tour_announcements']['message']
        
        self.logs_channel_id = channels_data['test']['logs']['channel']
        self.player_register_thread_id = channels_data['test']['logs']['threads']['player_register']
        self.player_change_amq_thread_id = channels_data['test']['logs']['threads']['player_change_amq']
        self.player_change_rank_thread_id = channels_data['test']['logs']['threads']['player_change_rank']
        self.player_change_ban_thread_id = channels_data['test']['logs']['threads']['player_change_ban']
        self.gamemode_add_thread_id = channels_data['test']['logs']['threads']['gamemode_add']
        self.gamemode_delete_thread_id = channels_data['test']['logs']['threads']['gamemode_delete']
        self.gamemode_edit_thread_id = channels_data['test']['logs']['threads']['gamemode_edit']
        self.commands_usage_thread_id = channels_data['test']['logs']['threads']['commands_usage']
        self.scheduled_tours_add_thread_id = channels_data['test']['logs']['threads']['scheduled_tours_add']
        self.scheduled_tours_delete_thread_id = channels_data['test']['logs']['threads']['scheduled_tours_delete']
        self.scheduled_tours_edit_thread_id = channels_data['test']['logs']['threads']['scheduled_tours_edit']


    def get_main_guild(self, client: discord.Client) -> discord.Guild:
        """Return the main guild object."""
        return client.get_guild(self.main_guild_id)
    
    def get_test_guild(self, client: discord.Client) -> discord.Guild:
        """Return the test guild object."""
        return client.get_guild(self.test_guild_id)
    
    def get_new_guild(self, client: discord.Client) -> discord.Guild:       # NOTE Remove when moved
        """Return the new guild object."""
        return client.get_guild(self.new_guild_id)
    
    def get_guild(self, client: discord.Client, guild_id: int) -> discord.Guild:
        """Return the guild object given the `guild_id` argument."""
        match guild_id:
            case self.main_guild_id:
                return self.get_main_guild(client)
            case self.new_guild_id:                                         # NOTE Remove when moved
                return self.get_new_guild(client)
            case self.test_guild_id:
                return self.get_test_guild(client)
            case _:
                raise ValueError('Unsupported guild provided')


    def get_host_channel(self, client: discord.Client) -> discord.TextChannel:
        """Return the host channel object (from the main guild)."""
        main_guild = self.get_main_guild(client)
        return main_guild.get_channel(self.host_channel_id)
    
    # NOTE Remove when moved
    def get_new_host_channel(self, client: discord.Client) -> discord.TextChannel:
        """Return the host channel object (from the new guild)."""
        new_guild = self.get_new_guild(client)
        return new_guild.get_channel(self.new_host_channel_id)

    def get_feedback_channel(self, client: discord.Client) -> discord.TextChannel:
        """Return the feedback channel object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        return test_guild.get_channel(self.feedback_channel_id)
    
    def get_report_channel(self, client: discord.Client) -> discord.TextChannel:
        """Return the report channel object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        return test_guild.get_channel(self.report_channel_id)
    
    def get_picks_channel(self, client: discord.Client) -> discord.TextChannel:
        """Return the picks channel object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        return test_guild.get_channel(self.picks_channel_id)


    def get_main_tour_announcements_channel(self, client: discord.Client) -> discord.TextChannel:
        """Return the tour announcements channel object (from the main guild)."""
        new_guild = self.get_new_guild(client)      # NOTE Change to Main for consistance when fully moved
        return new_guild.get_channel(self.tour_announcements_channel_id)

    def get_main_tour_announcements_message(self, client: discord.Client) -> discord.Message:
        """Return the tour announcements message object (from the main guild)."""
        tour_announcements_channel = self.get_main_tour_announcements_channel(client)
        return tour_announcements_channel.get_partial_message(self.tour_announcements_message_id)
    
    def get_test_tour_announcements_channel(self, client: discord.Client) -> discord.TextChannel:
        """Return the tour announcements channel object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        return test_guild.get_channel(self.test_tour_announcements_channel_id)

    def get_test_tour_announcements_message(self, client: discord.Client) -> discord.Message:
        """Return the tour announcements message object (from the test guild)."""
        test_tour_announcements_channel = self.get_test_tour_announcements_channel(client)
        return test_tour_announcements_channel.get_partial_message(self.test_tour_announcements_message_id)

    def get_tour_announcements_message(self, client: discord.Client, guild_id: int) -> discord.Message:
        """Return the tour announcements message object (from the main/test guild depending on the `guild_id` value)."""
        match guild_id:
            case self.new_guild_id:         # NOTE Change to main when moved
                return self.get_main_tour_announcements_message(client)
            case self.test_guild_id:
                return self.get_test_tour_announcements_message(client)
            case _:
                raise ValueError('Unsupported guild provided')


    def get_logs_channel(self, client: discord.Client) -> discord.TextChannel:
        """Return the logs channel object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        return test_guild.get_channel(self.logs_channel_id)

    async def get_player_register_thread(self, client: discord.Client) -> discord.Thread:
        """Return the `/player_register` command's log thread object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        # NOTE not using guild.get_thread as if the thread is archived, it isn't stored in the cache (will return `None`)
        thread = await test_guild.fetch_channel(self.player_register_thread_id)
        return thread

    async def get_player_change_amq_thread(self, client: discord.Client) -> discord.Thread:
        """Return the `/player_change_amq` command's log thread object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        # NOTE not using guild.get_thread as if the thread is archived, it isn't stored in the cache (will return `None`)
        thread = await test_guild.fetch_channel(self.player_change_amq_thread_id)
        return thread

    async def get_player_change_rank_thread(self, client: discord.Client) -> discord.Thread:
        """Return the `/player_change_rank` command's log thread object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        # NOTE not using guild.get_thread as if the thread is archived, it isn't stored in the cache (will return `None`)
        thread = await test_guild.fetch_channel(self.player_change_rank_thread_id)
        return thread
    
    async def get_player_change_ban_thread(self, client: discord.Client) -> discord.Thread:
        """Return the `/player_change_ban` command's log thread object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        # NOTE not using guild.get_thread as if the thread is archived, it isn't stored in the cache (will return `None`)
        thread = await test_guild.fetch_channel(self.player_change_ban_thread_id)
        return thread

    async def get_gamemode_add_thread(self, client: discord.Client) -> discord.Thread:
        """Return the `/gamemode_add` command's log thread object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        # NOTE not using guild.get_thread as if the thread is archived, it isn't stored in the cache (will return `None`)
        thread = await test_guild.fetch_channel(self.gamemode_add_thread_id)
        return thread

    async def get_gamemode_delete_thread(self, client: discord.Client) -> discord.Thread:
        """Return the `/gamemode_delete` command's log thread object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        # NOTE not using guild.get_thread as if the thread is archived, it isn't stored in the cache (will return `None`)
        thread = await test_guild.fetch_channel(self.gamemode_delete_thread_id)
        return thread

    async def get_gamemode_edit_thread(self, client: discord.Client) -> discord.Thread:
        """Return the `/gamemode_edit` command's log thread object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        # NOTE not using guild.get_thread as if the thread is archived, it isn't stored in the cache (will return `None`)
        thread = await test_guild.fetch_channel(self.gamemode_edit_thread_id)
        return thread
    
    async def get_commands_usage_thread(self, client: discord.Client) -> discord.Thread:
        """Return the log thread object (from the test guild) used for keeping track of important (mainly tour) commands."""
        test_guild = self.get_test_guild(client)
        # NOTE not using guild.get_thread as if the thread is archived, it isn't stored in the cache (will return `None`)
        thread = await test_guild.fetch_channel(self.commands_usage_thread_id)
        return thread
    
    async def get_scheduled_tours_add_thread(self, client: discord.Client) -> discord.Thread:
        """Return the `/schedule_tour_add` command's log thread object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        # NOTE not using guild.get_thread as if the thread is archived, it isn't stored in the cache (will return `None`)
        thread = await test_guild.fetch_channel(self.scheduled_tours_add_thread_id)
        return thread
    
    async def get_scheduled_tours_delete_thread(self, client: discord.Client) -> discord.Thread:
        """Return the `/schedule_tour_delete` command's log thread object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        # NOTE not using guild.get_thread as if the thread is archived, it isn't stored in the cache (will return `None`)
        thread = await test_guild.fetch_channel(self.scheduled_tours_delete_thread_id)
        return thread
    
    async def get_scheduled_tours_edit_thread(self, client: discord.Client) -> discord.Thread:
        """Return the `/schedule_tour_edit` command's log thread object (from the test guild)."""
        test_guild = self.get_test_guild(client)
        # NOTE not using guild.get_thread as if the thread is archived, it isn't stored in the cache (will return `None`)
        thread = await test_guild.fetch_channel(self.scheduled_tours_edit_thread_id)
        return thread
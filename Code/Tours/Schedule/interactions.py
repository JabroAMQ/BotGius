import discord

from Code.Utilities.error_handler import error_handler_decorator
from Code.Others.channels import Channels
from Code.Tours.Schedule.controller import Scheduled_Tour_Controller


async def _update_tour_announcements_message(interaction: discord.Interaction, fake_ping: bool = False) -> None:
    """Update the tour announcements message with the current scheduled tours."""
    scheduled_tours = Scheduled_Tour_Controller().represent_all_scheduled_tours(interaction.guild_id)
    scheduled_tours_message = Channels().get_tour_announcements_message(interaction.client, interaction.guild_id)
    await scheduled_tours_message.edit(content=scheduled_tours)

    # Send and delete an "empty" message to create a notification in the channel
    if fake_ping:
        await scheduled_tours_message.channel.send(content='.', delete_after=1)


@error_handler_decorator()
async def schedule_tour_add_interaction(interaction: discord.Interaction, description: str, timestamp: str, host: str):
    """Interaction to handle the `/schedule_tour_add` command. It creates a new scheduled_tour and stores it in the sheduled_tours's catalog."""
    await interaction.response.defer(ephemeral=True)

    # Set a fixed max scheduled tours number (25) to match Discord's select menu limit
    if Scheduled_Tour_Controller().count_scheduled_tours(interaction.guild_id) >= 25:
        content = 'The maximum number of scheduled tours (25) has been reached. Please delete some scheduled tours before adding new ones.'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    # Add the scheduled tour
    added, log = Scheduled_Tour_Controller().add_scheduled_tour(interaction.guild_id, description, host, timestamp)
    if not added:
        content = 'There was an error while scheduling the tour'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    await _update_tour_announcements_message(interaction, fake_ping=True)
    
    # Log the addition of the gamemode
    log_thread = await Channels().get_scheduled_tours_add_thread(interaction.client)
    guild = Channels().get_guild(interaction.client, interaction.guild_id)
    content = f'A new tour was scheduled by {interaction.user.mention} in **{guild.name}**:\n{log}'
    await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())
    await interaction.followup.send(content='Tour scheduled successfully', ephemeral=True)


@error_handler_decorator()
async def schedule_tour_delete_interaction(interaction: discord.Interaction):
    """Interaction to handle the `/schedule_tour_delete` command. It deletes a scheduled_tour from the sheduled_tours's catalog."""
    await interaction.response.defer(ephemeral=True)

    class Confirm_View(discord.ui.View):
        def __init__(self, id: int):
            super().__init__(timeout=180)
            self.id = id

        @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
        async def confirm(self, new_interaction: discord.Interaction, _: discord.ui.Button):
            await new_interaction.response.defer(ephemeral=True)

            # Delete the scheduled tour
            deleted, log = Scheduled_Tour_Controller().delete_scheduled_tour(self.id)
            if not deleted:
                content = 'There was an error while deleting the Scheduled_Tour'
                await new_interaction.followup.send(content=content, ephemeral=True)
                return
            
            # NOTE We do not notify when deleting a tour. Change if desired
            await _update_tour_announcements_message(new_interaction, fake_ping=False)

            # Log the deletion of the gamemode
            log_thread = await Channels().get_scheduled_tours_delete_thread(new_interaction.client)
            guild = Channels().get_guild(new_interaction.client, new_interaction.guild_id)
            content = f'A scheduled tour was deleted by {new_interaction.user.mention} in **{guild.name}**:\n{log}'
            await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())

            content = 'Scheduled Tour deleted successfully'
            await new_interaction.followup.send(content=content, ephemeral=True)
            self.stop()


    class Scheduled_Tour_Dropdown(discord.ui.Select):
        def __init__(self, scheduled_tours: list[tuple[str, int]]):
            options = [discord.SelectOption(label=scheduled_tour[0], value=str(scheduled_tour[1])) for scheduled_tour in scheduled_tours]
            super().__init__(placeholder='Choose a Scheduled Tour', options=options)
            self.options = options  # We can't stablished self.options before calling super().__init__()

        async def callback(self, new_interaction: discord.Interaction):
            selected_value = self.values[0]
            id = int(selected_value)
            selected_tour = next(opt.label for opt in self.options if opt.value == selected_value)
            content = f'Confirm you want to apply the changes to the tour selected:\n{selected_tour}'
            await new_interaction.response.send_message(content=content, view=Confirm_View(id), ephemeral=True)


    class Scheduled_Tour_Dropdown_View(discord.ui.View):
        def __init__(self, scheduled_tours: list[tuple[str, int]]):
            super().__init__(timeout=180)
            self.add_item(Scheduled_Tour_Dropdown(scheduled_tours))


    # Get all the scheduled tours
    scheduled_tours = Scheduled_Tour_Controller().get_all_scheduled_tours(interaction.guild_id)
    if not scheduled_tours:
        content = 'There are no scheduled tours to delete'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    # Select the tour to delete
    view = Scheduled_Tour_Dropdown_View(scheduled_tours)
    await interaction.followup.send(content='Select the Scheduled Tour to delete', view=view, ephemeral=True)


@error_handler_decorator()
async def schedule_tour_edit_interaction(interaction: discord.Interaction, description: str = None, timestamp: int = None, host: str = None):
    """Interaction to handle the `/schedule_tour_edit` command. It edits a scheduled_tour from the sheduled_tours's catalog."""
    await interaction.response.defer(ephemeral=True)

    class Confirm_View(discord.ui.View):
        def __init__(self, id: int, description: str = None, timestamp: int = None, host: str = None):
            super().__init__(timeout=180)
            self.id = id
            self.description = description
            self.timestamp = timestamp
            self.host = host

        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def confirm(self, new_interaction: discord.Interaction, _: discord.ui.Button):
            await new_interaction.response.defer(ephemeral=True)

            # Edit the scheduled tour
            edited, log = Scheduled_Tour_Controller().edit_scheduled_tour(self.id, self.description, self.host, self.timestamp)
            if not edited:
                content = 'There was an error while editing the Scheduled_Tour'
                await new_interaction.followup.send(content=content, ephemeral=True)
                return
            
            await _update_tour_announcements_message(new_interaction, fake_ping=True)

            # Log the edition of the gamemode
            log_thread = await Channels().get_scheduled_tours_edit_thread(new_interaction.client)
            guild = Channels().get_guild(new_interaction.client, new_interaction.guild_id)
            content = f'A scheduled tour was edited by {new_interaction.user.mention} in **{guild.name}**:\n{log}'
            await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())

            content = 'Scheduled Tour edited successfully'
            await new_interaction.followup.send(content=content, ephemeral=True)
            self.stop()


    class Scheduled_Tour_Dropdown(discord.ui.Select):
        def __init__(self, scheduled_tours: list[tuple[str, int]], description: str = None, timestamp: int = None, host: str = None):
            options = [discord.SelectOption(label=scheduled_tour[0], value=str(scheduled_tour[1])) for scheduled_tour in scheduled_tours]
            super().__init__(placeholder='Choose a Scheduled Tour', options=options)
            self.description = description
            self.timestamp = timestamp
            self.host = host
            self.options = options  # We can't stablished self.options before calling super().__init__()

        async def callback(self, new_interaction: discord.Interaction):
            selected_value = self.values[0]
            id = int(selected_value)
            selected_tour = next(opt.label for opt in self.options if opt.value == selected_value)
            content = f'Confirm you want to apply the changes to the tour selected:\n{selected_tour}'
            await new_interaction.response.send_message(content=content, view=Confirm_View(id, description, timestamp, host), ephemeral=True)


    class Scheduled_Tour_Dropdown_View(discord.ui.View):
        def __init__(self, scheduled_tours: list[tuple[str, int]], description: str = None, timestamp: int = None, host: str = None):
            super().__init__(timeout=180)
            self.add_item(Scheduled_Tour_Dropdown(scheduled_tours, description, timestamp, host))


    # Get all the scheduled tours
    scheduled_tours = Scheduled_Tour_Controller().get_all_scheduled_tours(interaction.guild_id)
    if not scheduled_tours:
        content = 'There are no scheduled tours to edit'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    # Check if at least one value has been provided
    if not description and not timestamp and not host:
        content = 'At least one field must be provided'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    # Select the tour to edit
    view = Scheduled_Tour_Dropdown_View(scheduled_tours, description, timestamp, host)
    await interaction.followup.send(content='Select the Scheduled Tour to edit with the provided changes', view=view, ephemeral=True)
import discord

from Code.Utilities.error_handler import error_handler_decorator
from Code.Others.channels import Channels
from Code.Tours.Schedule.controller import Scheduled_Tour_Controller


async def _update_tour_announcements_message(client: discord.Client, fake_ping: bool = False) -> None:
    """Update the tour announcements message with the current scheduled tours."""
    scheduled_tours = Scheduled_Tour_Controller().represent_all_scheduled_tours()
    scheduled_tours_message = Channels().get_tour_announcements_message(client)
    await scheduled_tours_message.edit(content=scheduled_tours)

    # Send and delete an "empty" message to create a notification in the channel
    if fake_ping:
        await scheduled_tours_message.channel.send(content='.', delete_after=1)


@error_handler_decorator()
async def schedule_tour_add_interaction(interaction: discord.Interaction, description: str, timestamp: str, host: str):
    """Interaction to handle the `/schedule_tour_add` command. It creates a new scheduled_tour and stores it in the sheduled_tours's catalog."""
    await interaction.response.defer(ephemeral=True)

    # Set a fixed max scheduled tours number (25) to match Discord's select menu limit
    if Scheduled_Tour_Controller().count_scheduled_tours() >= 25:
        content = 'The maximum number of scheduled tours (25) has been reached. Please delete some scheduled tours before adding new ones.'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    # Add the scheduled tour
    added, log = Scheduled_Tour_Controller().add_scheduled_tour(description, host, timestamp)
    if not added:
        content = 'There was an error when scheduling the tour'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    await _update_tour_announcements_message(interaction.client, fake_ping=True)
    
    # Log the addition of the gamemode
    log_thread = await Channels().get_scheduled_tours_add_thread(interaction.client)
    content = f'A new tour was scheduled by {interaction.user.mention}:\n{log}'
    await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())
    await interaction.followup.send(content='Tour scheduled successfully', ephemeral=True)


@error_handler_decorator()
async def schedule_tour_delete_interaction(interaction: discord.Interaction):
    """Interaction to handle the `/schedule_tour_delete` command. It deletes a scheduled_tour from the sheduled_tours's catalog."""
    await interaction.response.defer(ephemeral=True)

    class Scheduled_Tour_Dropdown(discord.ui.Select):
        def __init__(self, scheduled_tours: list[tuple[str, int]]):
            options = [discord.SelectOption(label=scheduled_tour[0], value=scheduled_tour[1]) for scheduled_tour in scheduled_tours]
            super().__init__(placeholder='Choose a Scheduled Tour', options=options)

        async def callback(self, new_interaction: discord.Interaction):
            await new_interaction.response.defer(ephemeral=True)

            # Delete the scheduled tour
            deleted, log = Scheduled_Tour_Controller().delete_scheduled_tour(int(self.values[0]))
            if not deleted:
                content = 'There was an error when deleting the Scheduled_Tour'
                await new_interaction.followup.send(content=content, ephemeral=True)
                return
            
            # NOTE We do not notify when deleting a tour. Change if desired
            await _update_tour_announcements_message(new_interaction.client, fake_ping=False)

            # Log the deletion of the gamemode
            log_thread = await Channels().get_scheduled_tours_delete_thread(new_interaction.client)
            content = f'A scheduled tour was deleted by {new_interaction.user.mention}\n{log}'
            await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())

            content = 'Scheduled Tour deleted successfully'
            await new_interaction.followup.send(content=content, ephemeral=True)


    class Scheduled_Tour_Dropdown_View(discord.ui.View):
        def __init__(self, scheduled_tours: list[tuple[str, int]]):
            super().__init__(timeout=180)
            self.add_item(Scheduled_Tour_Dropdown(scheduled_tours))


    # Get all the scheduled tours
    scheduled_tours = list(Scheduled_Tour_Controller().get_all_scheduled_tours())
    if not scheduled_tours:
        content = 'There are no scheduled tours to delete'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    # Select the tour to delete
    view = Scheduled_Tour_Dropdown_View(scheduled_tours)
    await interaction.followup.send(content='Select the Scheduled Tour to delete:', view=view, ephemeral=True)
import discord

from Code.Utilities.error_handler import error_handler_decorator
from Code.Others.channels import Channels
from Code.Tours.Schedule.controller import Scheduled_Tour_Controller


async def _update_tour_announcements_message(interaction: discord.Interaction, fake_ping: bool = False) -> None:
    """Update the tour announcements message with the current scheduled tours."""
    scheduled_tours = Scheduled_Tour_Controller().represent_all_scheduled_tours(interaction.guild_id)
    scheduled_tours_message = await Channels().get_tour_announcements_message(interaction.client, interaction.guild_id)
    await scheduled_tours_message.edit(content=scheduled_tours)

    # Send and delete an "empty" message to create a notification in the channel
    if fake_ping:
        await scheduled_tours_message.channel.send(content='.', delete_after=1)


@error_handler_decorator()
async def schedule_tour_add_interaction(interaction: discord.Interaction, description: str, timestamp: str, host: str):
    """Interaction to handle the `/schedule_tour_add` command. It creates a new scheduled_tour and stores it in the sheduled_tours's catalog."""
    await interaction.response.defer(ephemeral=True)

    add_ok = await Scheduled_Tour_Controller().allow_additions(interaction)
    if not add_ok:
        content = 'We are already too close to the discord\'s message length limit (2000 characters). If you ever see this, notify it to look for solutions'
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
async def schedule_tour_delete_interaction(interaction: discord.Interaction, fixed_id: int):
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


    # Get the scheduled tour, ensuring fixed_id exists
    exists, tour = Scheduled_Tour_Controller().get_tour_from_fixed_id(interaction.guild_id, fixed_id)
    if not exists:
        content = 'A scheduled tour with the given ID couldn\'t be found'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    # Delete the tour
    content = f'Confirm you want to delete the next scheduled tour:\n{repr(tour)}'
    await interaction.followup.send(content=content, view=Confirm_View(tour.id), ephemeral=True)
    return


@error_handler_decorator()
async def schedule_tour_edit_interaction(interaction: discord.Interaction, fixed_id: int, description: str = None, timestamp: int = None, host: str = None):
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


    # Check if at least one value has been provided
    if not description and not timestamp and not host:
        content = 'At least one field must be provided'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    # Get the scheduled tour, ensuring fixed_id exists
    exists, tour = Scheduled_Tour_Controller().get_tour_from_fixed_id(interaction.guild_id, fixed_id)
    if not exists:
        content = 'A scheduled tour with the given ID couldn\'t be found'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    edit_ok = await Scheduled_Tour_Controller().allow_modifications(interaction, fixed_id, description, timestamp, host)
    if not edit_ok:
        content = 'Applying these changes will reach discord\'s message length limit (2000 characters). If you ever see this, notify it to look for solutions'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    # Edit the tour
    content = f'Confirm you want to apply the changes provided to the next scheduled tour:\n{repr(tour)}'
    await interaction.followup.send(content=content, view=Confirm_View(tour.id, description, timestamp, host), ephemeral=True)
    return
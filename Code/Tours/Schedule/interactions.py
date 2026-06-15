import discord

from Code.Utilities.error_handler import error_handler_decorator
from Code.Others.channels import Channels
from Code.Tours.Schedule.controller import Scheduled_Tour_Controller
from Code.Tours.Schedule.displayer import Scheduled_Tour_Messages_Displayer


@error_handler_decorator()
async def schedule_tour_add_interaction(interaction: discord.Interaction, description: str, timestamp: str, host: str):
    """Interaction to handle the `/schedule_tour_add` command. It creates a new scheduled_tour and stores it in the sheduled_tours's catalog."""
    await interaction.response.defer(ephemeral=True)
    
    # Add the scheduled tour
    added, log = Scheduled_Tour_Controller().add_scheduled_tour(interaction.guild_id, description, host, timestamp)
    if not added:
        content = 'There was an error while scheduling the tour'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    await Scheduled_Tour_Messages_Displayer().refresh_scheduled_tours_messages(interaction.client, interaction.guild_id, fake_ping=True)
    
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
            await Scheduled_Tour_Messages_Displayer().refresh_scheduled_tours_messages(new_interaction.client, new_interaction.guild_id, fake_ping=False)

            # Log the deletion of the gamemode
            log_thread = await Channels().get_scheduled_tours_delete_thread(new_interaction.client)
            guild = Channels().get_guild(new_interaction.client, new_interaction.guild_id)
            content = f'A scheduled tour was deleted by {new_interaction.user.mention} in **{guild.name}**:\n{log}'
            await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())

            content = 'Scheduled Tour deleted successfully'
            await new_interaction.followup.send(content=content, ephemeral=True)
            self.stop()


    # Get the scheduled tour, ensuring fixed_id exists
    exists, tour = Scheduled_Tour_Messages_Displayer().get_tour_from_fixed_id(interaction.guild_id, fixed_id)
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
            
            await Scheduled_Tour_Messages_Displayer().refresh_scheduled_tours_messages(new_interaction.client, new_interaction.guild_id, fake_ping=True)

            # Log the edition of the tour
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
    exists, tour = Scheduled_Tour_Messages_Displayer().get_tour_from_fixed_id(interaction.guild_id, fixed_id)
    if not exists:
        content = 'A scheduled tour with the given ID couldn\'t be found'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    # Edit the tour
    content = f'Confirm you want to apply the changes provided to the next scheduled tour:\n{repr(tour)}'
    await interaction.followup.send(content=content, view=Confirm_View(tour.id, description, timestamp, host), ephemeral=True)
    return
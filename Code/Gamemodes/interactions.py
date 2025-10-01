import discord

from Code.Utilities.error_handler import error_handler_decorator
from Code.Gamemodes.controller import Main_Controller
from Code.Gamemodes.Gamemodes.gamemode import Gamemode
from Code.Rolls.basic_rolls import Roll
from Code.Rolls.enums import Rolls_Enum, Roll_Gamemode
from Code.Others.channels import Channels

@error_handler_decorator()
async def gamemode_add(
    interaction: discord.Interaction,
    gamemode_name: str,
    gamemode_size: int,
    gamemode_code: str,
    is_gamemode_watched: bool,
    is_random_dist_rollable: bool,
    is_weighted_dist_rollable: bool,
    is_equal_dist_rollable: bool
):
    """Interaction to handle the `/gamemode_add` command. It stores in the gamemodes's Database and Catalog the new gamemode created with the provided information."""
    await interaction.response.defer(ephemeral=True)

    has_gamemode_been_added, log = Main_Controller().add_gamemode(
        gamemode_name=gamemode_name,
        gamemode_size=gamemode_size,
        gamemode_code=gamemode_code,
        is_gamemode_watched=is_gamemode_watched,
        is_random_dist_rollable=is_random_dist_rollable,
        is_weighted_dist_rollable=is_weighted_dist_rollable,
        is_equal_dist_rollable=is_equal_dist_rollable
    )

    if not has_gamemode_been_added:
        await interaction.followup.send(content='The gamemode could not been added as there is already a gamemode registered with that name.', ephemeral=True)
        return

    # Log the addition of the gamemode
    log_thread = await Channels().get_gamemode_add_thread(interaction.client)
    content = f'Added gamemode by {interaction.user.mention}:\n{log}'
    await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())
    await interaction.followup.send(content='Gamemode added successfully!', ephemeral=True)

@error_handler_decorator()
async def gamemode_delete(interaction: discord.Interaction, gamemode_name: str):
    """Interaction to handle the `/gamemode_delete` command. It deletes from the gamemodes's Database and Catalog the gamemode which has the name provided."""
    
    class confirm_elimination_view(discord.ui.View):
        def __init__(self, gamemode: Gamemode):
            super().__init__(timeout=60)
            self.gamemode = gamemode
            self.already_deleted = False
        
        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        @error_handler_decorator()
        async def confirm(self, new_interaction: discord.Interaction, _ = discord.Button):
            await new_interaction.response.defer(ephemeral=True)
            if self.already_deleted:
                await new_interaction.followup.send(content='The gamemode has already been deleted', ephemeral=True)
                return

            # Delete gamemode
            Main_Controller().delete_gamemode(self.gamemode)
            self.already_deleted = True

            # Send log and confirmation messages
            log_thread = await Channels().get_gamemode_delete_thread(new_interaction.client)
            content = f'Deleted gamemode by {new_interaction.user.mention}:\n{gamemode.display_all_details()}'
            await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())
            await new_interaction.followup.send(content='Gamemode deleted successfully!', ephemeral=True)
    
    await interaction.response.defer(ephemeral=True) 
    gamemode = Main_Controller().get_gamemode(gamemode_name)
    if gamemode is None:
        await interaction.followup.send(content=f'A similar enough gamemode name to **{gamemode_name}** couldn\'t be found')
        return
    
    content = f'The next gamemode will be deleted: **{gamemode.name}**.\nClick on the button to confirm it.'
    view = confirm_elimination_view(gamemode)
    await interaction.followup.send(content=content, view=view, ephemeral=True)


@error_handler_decorator()
async def gamemode_edit(
    interaction: discord.Interaction,
    gamemode_name: str,
    new_name: str | None,
    new_code: str | None,
    new_random_song_distribution: bool | None,
    new_weighted_song_distribution: bool | None,
    new_equal_song_distribution: bool | None,
):
    """Interaction to handle the `/gamemode_edit` command. It display a select menu where the user can choose what gamemode's property to edit (and edit it afterwards)."""

    class confirm_changes_view(discord.ui.View):
        def __init__(
            self,
            gamemode: Gamemode,
            name: str | None,
            code: str | None,
            random_distribution: bool | None,
            weighted_distribution: bool | None,
            equal_distribution: bool | None,
            content: str
        ):
            super().__init__(timeout=60)
            self.gamemode = gamemode
            self.name = name
            self.code = code
            self.random_distribution = random_distribution
            self.weighted_distribution = weighted_distribution
            self.equal_distribution = equal_distribution

            self.log_content = content
            self.changes_already_applied = False
        
        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        @error_handler_decorator()
        async def confirm(self, new_interaction: discord.Interaction, _ = discord.Button):
            await new_interaction.response.defer(ephemeral=True)
            if self.changes_already_applied:
                await new_interaction.followup.send(content='The changes have already been applied', ephemeral=True)
                return
            self.changes_already_applied = True

            # Edit the gamemode
            changes_applied = Main_Controller().edit_gamemode(
                gamemode_name=self.gamemode.name,
                new_name=self.name,
                new_code=self.code,
                new_random_dist_rollable=self.random_distribution,
                new_weighted_dist_rollable=self.weighted_distribution,
                new_equal_dist_rollable=self.equal_distribution
            )

            if not changes_applied:
                await new_interaction.followup.send(content='An error was raised when applying the changes...', ephemeral=True)
                return

            # Send the log message
            log_thread = await Channels().get_gamemode_edit_thread(new_interaction.client)
            await log_thread.send(content=self.log_content, allowed_mentions=discord.AllowedMentions.none())
            await new_interaction.followup.send(content='Gamemode modified successfully!', ephemeral=True)

    await interaction.response.defer(ephemeral=True)

    # Get the gamemode
    gamemode = Main_Controller().get_gamemode(gamemode_name)
    if gamemode is None:
        await interaction.followup.send(content=f'A similar enough gamemode name to **{gamemode_name}** couldn\'t be found')
        return
    
    # For the fields which values are trying to be changed, get the old values stored
    invalid, name, code, random, weighted, equal = Main_Controller().get_gamemode_old_values(
        gamemode=gamemode,
        new_name=new_name,
        new_code=new_code,
        new_random=new_random_song_distribution,
        new_weighted=new_weighted_song_distribution,
        new_equal=new_equal_song_distribution
    )
    
    # Check for invalud values combination
    if invalid:
        await interaction.followup.send(content='Changes cannot be applied as for `Song Selection = True`, at least one distribution must be `True` as well', ephemeral=True)
        return

    # Get the log message
    changes_content = _get_gamemode_edit_log(
        old_name=name, old_code=code, old_random_distribution=random, old_weighted_distribution=weighted, old_equal_distribution=equal, new_name=new_name,
        new_code=new_code, new_random_distribution=new_random_song_distribution, new_weighted_distribution=new_weighted_song_distribution,
        new_equal_distribution=new_equal_song_distribution
    )

    # Check if there is at least one valid change
    if not changes_content:
        content = 'At least one new (different than current) value must be provided!'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    # Send the response with the confirmation button
    confirm_content = f'Gamemode selected: **{gamemode.name}**\nThese changes will be applied:\n{changes_content}'
    log_content = f'Edited gamemode **{gamemode.name}** by {interaction.user.mention}:\n{changes_content}'
    view = confirm_changes_view(
        gamemode=gamemode,
        name=new_name,
        code=new_code,
        random_distribution=new_random_song_distribution,
        weighted_distribution=new_weighted_song_distribution,
        equal_distribution=new_equal_song_distribution,
        content=log_content
    )
    await interaction.followup.send(content=confirm_content, view=view, ephemeral=True)


@error_handler_decorator()
async def get_code(interaction: discord.Interaction, gamemode_name: str):
    """Interaction to handle the `/gamemode_code` command. It returns the code of the gamemode asked for with a button that allows to display its description when clicked."""
    
    class get_info_view(discord.ui.View):
        def __init__(self, gamemode: Gamemode):
            super().__init__(timeout=60)
            self.gamemode = gamemode

        @discord.ui.button(label='info', style=discord.ButtonStyle.green)
        @error_handler_decorator()
        async def get_info(self, new_interaction: discord.Interaction, _: discord.ui.Button):
            await new_interaction.response.defer()
            new_content = self.gamemode.display_info_details()
            await new_interaction.followup.send(content=new_content)


    await interaction.response.defer()
    gamemode = Main_Controller().get_gamemode(gamemode_name)
    if gamemode is None:
        content = f'A similar enough gamemode name to **{gamemode_name}** couldn\'t be found'
        await interaction.followup.send(content=content)
        return

    content = gamemode.display_code_details()
    view = get_info_view(gamemode=gamemode)
    await interaction.followup.send(content=content, view=view)


@error_handler_decorator()
async def get_info(interaction: discord.Interaction, gamemode_name: str):
    """Interaction to handle the `/gamemode_info` command. It returns the description of the gamemode asked for with a button that allows to display its code when clicked."""
    
    class get_code_view(discord.ui.View):
        def __init__(self, gamemode: Gamemode):
            super().__init__(timeout=60)
            self.gamemode = gamemode

        @discord.ui.button(label='code', style=discord.ButtonStyle.green)
        @error_handler_decorator()
        async def get_code(self, new_interaction: discord.Interaction, _: discord.ui.Button):
            await new_interaction.response.defer()
            new_content = self.gamemode.display_code_details()
            await new_interaction.followup.send(content=new_content)
    
    
    await interaction.response.defer()
    gamemode = Main_Controller().get_gamemode(gamemode_name)
    if gamemode is None:
        content = f'A similar enough gamemode name to **{gamemode_name}** couldn\'t be found'
        await interaction.followup.send(content=content)
        return

    content = gamemode.display_info_details()
    view = get_code_view(gamemode=gamemode)
    await interaction.followup.send(content=content, view=view)


@error_handler_decorator()
async def roll(interaction: discord.Interaction, type: int):
    """Interaction to handle the `/roll` command. It rolls a possible value given the type chosen."""
    await interaction.response.defer(ephemeral=False)
    enum_type = Rolls_Enum(type)
    roll = Roll.roll(enum_type, as_str=True)
    await interaction.followup.send(content=roll, ephemeral=False)


@error_handler_decorator()
async def roll_gamemode(interaction: discord.Interaction, type: int):
    """Interaction to handle the `/roll_gamemode` command. It rolls a possible gamemode given the type chosen."""
    
    class Roll_Gamemode_View(discord.ui.View):

        def __init__(self, gamemode: Gamemode) -> None:
            super().__init__(timeout=180)
            self.gamemode = gamemode

        @discord.ui.button(label='code', style=discord.ButtonStyle.green)
        @error_handler_decorator()
        async def get_code(self, new_interaction: discord.Interaction, _: discord.ui.Button):
            await new_interaction.response.defer()
            new_content = self.gamemode.display_code_details()
            await new_interaction.followup.send(content=new_content)

        @discord.ui.button(label='info', style=discord.ButtonStyle.green)
        @error_handler_decorator()
        async def get_info(self, new_interaction: discord.Interaction, _: discord.ui.Button):
            await new_interaction.response.defer()
            new_content = self.gamemode.display_info_details()
            await new_interaction.followup.send(content=new_content)
    

    await interaction.response.defer(ephemeral=False)
    enum_type = Roll_Gamemode(type)
    gamemode = Roll.roll_gamemode(enum_type)
    
    content = f'**{enum_type.name.replace("_", " ").capitalize()} rolled:** {gamemode.name}\n{gamemode.roll_distribution()}'
    view = Roll_Gamemode_View(gamemode)
    await interaction.followup.send(content=content, view=view, ephemeral=False)


def _get_gamemode_edit_log(
    old_name: str | None,
    new_name: str | None,
    old_code: str | None,
    new_code: str | None,
    old_random_distribution: bool | None,
    new_random_distribution: bool | None,
    old_weighted_distribution: bool | None,
    new_weighted_distribution: bool | None,
    old_equal_distribution: bool | None,
    new_equal_distribution: bool | None
) -> str:
    """Auxiliar method to get the log content of the `/gamemode_edit` interaction."""
    content = f'**Name**:\n- **Old:** `{old_name}`\n- **New:** `{new_name}`\n' if old_name is not None else ''
    content += f'**Random Distribution**:\n- **Old:** `{old_random_distribution}`\n- **New:** `{new_random_distribution}`\n' if old_random_distribution is not None else ''
    content += f'**Weighted Distribution**:\n- **Old:** `{old_weighted_distribution}`\n- **New:** `{new_weighted_distribution}`\n' if old_weighted_distribution is not None else ''
    content += f'**Equal Distribution**:\n- **Old:** `{old_equal_distribution}`\n- **New:** `{new_equal_distribution}`\n' if old_equal_distribution is not None else ''
    content += f'**Code**:\n- **Old:**\n```{old_code}```\n- **New:**\n```{new_code}```\n' if old_code is not None else ''
    return content
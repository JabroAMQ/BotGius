import os
import secrets

import discord

def _generate_file_name() -> str:
    """Return an 8-byte (16-character) random hexadecimal string to use it as file name."""
    random_string = secrets.token_hex(nbytes=8)
    return f'{random_string}.txt'

async def send_message_as_file(interaction: discord.Interaction, message: str | list[str], forbidden_error: bool = True):
    """
    Given a discord's Interaction (`interaction`) and the content to send as response (`message`), creates a File with the `message` content and
    sends it via the `interaction`.
    """
    try:
        file_name = _generate_file_name()
        with open(file_name, 'w', encoding='utf-8') as fd:
            fd.write(message) if isinstance(message, str) else fd.write('\n'.join(message))
            file = discord.File(file_name)

        if forbidden_error:
            content = 'It seems that I cannot send you a dm with the answer. Here you have a file with its content instead:'
            await interaction.followup.send(content=content, file=file, ephemeral=True)
        else:
            await interaction.followup.send(file=file, ephemeral=True)

    finally:
        os.remove(file_name)
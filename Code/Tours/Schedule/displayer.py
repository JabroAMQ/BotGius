import discord

from Code.Tours.Schedule.schedule import Scheduled_Tour
from Code.Tours.Schedule.controller import Scheduled_Tour_Controller
from Code.Others.channels import Channels

class Scheduled_Tour_Messages_Displayer:
    """Class in charge of displaying the scheduled tours into different messages handling discord's max length limit message limitation."""
    _instance = None
    def __new__(cls):
        """Override the __new__ method to return the existing instance of the class if it exists or create a new instance if it doesn't exist yet.\n"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance
    
    def _set_data(self) -> None:
        """"""
        self.MAX_CHUNK_LENGTH = 1950

    def get_tour_from_fixed_id(self, guild_id: int, fixed_id: int) -> tuple[bool, Scheduled_Tour | None]:
        """
        The scheduled tour message looks like this:
            1. [optional_emoji]"timestamp_1" "description_1", "host_1"
            2. [optional_emoji]"timestamp_2" "description_2", "host_2"
            3. [optional_emoji]"timestamp_3" "description_3", "host_3"
            ...

        `fixed_id` is that first character(s) from each line (1, 2, 3...).\n
        Return a tuple[bool, Scheduled_Tour] containing whether the tour was found and the tour itself (if found only)
        """
        guild_scheduled_tours = Scheduled_Tour_Controller().get_all_scheduled_tours(guild_id)
        index = fixed_id - 1

        if 0 <= index < len(guild_scheduled_tours):
            tour = guild_scheduled_tours[index]
            return True, tour
        
        return False, None

    def _build_text_chunks(self, sorted_tours: list[Scheduled_Tour]) -> list[str]:
        """
        Split `sorted_tours` into strings based on the length.\n
        Each block will have a header/footer and may not exceed the `MAX_CHUNK_LENGTH` character limit.
        """
        chunks = []
        current_chunk = '**Upcoming Scheduled Tours**:\n\n'

        # Pre-calculate the footer so we can use it in the "not exceed max limit" comparations
        footer = f"\nLast updated: <t:{int(discord.utils.utcnow().timestamp())}:R>"
        
        for global_index, tour in enumerate(sorted_tours, start=1):
            line = f'{global_index}. {repr(tour)}\n'

            # Simulate theorical message length if we add this line
            theoretical_length = len(current_chunk + line)
            is_last_tour = (global_index == len(sorted_tours))
            if is_last_tour:
                theoretical_length += len(footer)

            # If max length is reached, we close the chunk and start a new one
            if theoretical_length > self.MAX_CHUNK_LENGTH:
                chunks.append(current_chunk)                
                current_chunk = ''
            
            current_chunk += line
            
        # Add the footer of the last chunck
        current_chunk += footer
        chunks.append(current_chunk)
        return chunks


    async def refresh_scheduled_tours_messages(self, client: discord.Client, guild_id: int, fake_ping: bool) -> None:
        """
        Fetch the bot's channel history and synchronize the messages with the calculated text chunks.
        Dynamically creates, edits, or deletes messages as required.
        """
        channel = Channels().get_tour_announcements_channel(client, guild_id)       

        sorted_tours = Scheduled_Tour_Controller().get_all_scheduled_tours(guild_id)
        text_chunks = self._build_text_chunks(sorted_tours)

        # Get the message(s) where the scheduled tours are displayed
        messages = [message async for message in channel.history(limit=5, oldest_first=True)]

        # NOTE The channel is only used by the bot, but we ensure the messages are written by the bot anyway
        bot_messages = [message for message in messages if message.author == client.user]
        first_msg = bot_messages[0] if bot_messages else None
        
        # Synchronize chunks with discord messages using a loop matching the maximum elements found
        max_loops = max(len(text_chunks), len(bot_messages))

        for i in range(max_loops):
            # We have space in the current message to add the new tour, we edit the current message
            if i < len(text_chunks) and i < len(bot_messages):
                await bot_messages[i].edit(content=text_chunks[i])
                
            # There is no space left in the current message to add a new tour, we create a new message
            elif i < len(text_chunks) and i >= len(bot_messages):
                if i == 0:
                    new_msg = await channel.send(content=text_chunks[i])
                    first_msg = new_msg
                else:
                    # Send the new messages as replies of the first (first_msg is guaranteed to exist here)
                    await channel.send(content=text_chunks[i], reference=first_msg, mention_author=False)
                
            # The current message is empty (no tours) and there is no more tours to be added, we delete the current message
            elif i >= len(text_chunks) and i < len(bot_messages):
                await bot_messages[i].delete()

        # Send and delete an "empty" message to create a notification in the channel
        if fake_ping:
            await channel.send(content='.', delete_after=1)
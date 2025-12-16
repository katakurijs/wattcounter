import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver

load_dotenv()
token = os.getenv('TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is online!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    channel_id = 1450218039625912390

    if message.channel.id == channel_id:
        try:
            current_number = int(message.content.strip())
        except ValueError:
            await message.delete()
            await message.channel.send(f"are you this stupid {message.author.mention}? the channel name is 'counter' and you're sending a word?", delete_after=5)
            return
        
        messages = [msg async for msg in message.channel.history(limit=2)]
        
        if len(messages) < 2:
            # This is the first or second message in the channel
            if current_number != 1:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Start with 1!", delete_after=5)
            return
        
        last_message = messages[1]  # messages[0] is the current message
        
        try:
            last_number = int(last_message.content.strip())
        except ValueError:
            # Previous message wasn't a number (shouldn't happen if bot is working correctly)
            last_number = 0
        
        # Check if the number is correct (last + 1)
        if current_number != last_number + 1:
            await message.delete()
            await message.channel.send(
                f"it's says 'counter' dumbass {message.author.mention} I'll help you, its {last_number + 1}",
                delete_after=5
            )
            return
        
        # Check if the sender is different from the last message sender
        if message.author.id == last_message.author.id:
            await message.delete()
            await message.channel.send(
                f"Can't keep the channel for yourself! {message.author.mention}",
                delete_after=5
            )
            return
        
        # All checks passed! Optionally add a reaction
        await message.add_reaction("✅")

webserver.keep_alive()
bot.run(token=token, log_handler=handler, log_level=logging.DEBUG)
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='<', intents=intents)

@client.event
async def on_ready():
    print(f"Logged in As {client.user}")

@client.event
async def on_message(message):
    # if the message is from the bot itself, ignore it
    if message.author == client.user:
        return

    if message.content.startswith('!join'):
        # the message is a command to join a voice channel, so we get the voice channel
        # that the user who sent the message is in
        user_voice_channel = message.author.voice.channel

        # if the user is not in a voice channel, we can't join it
        if user_voice_channel is None:
            await message.channel.send('You are not in a voice channel!')
            return

        # if the bot is already in a voice channel, we leave it first
        if client.voice_clients:
            await client.voice_clients[0].disconnect()

        # now we can join the user's voice channel
        await user_voice_channel.connect()

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
            channel = after.channel
            await channel.send(member.name, tts=True)

@client.command()
async def ping(ctx):
    await ctx.send('pong')

client.run(os.getenv('TOKEN'))
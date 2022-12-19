import os
import discord

from discord.utils import get
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from gtts import gTTS
from discord import FFmpegPCMAudio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='#', intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in As {bot.user}")


@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    member_name = str(member).split("#")[0]

    if len(bot.voice_clients) > 0:

        # Joined
        if before.channel is None and after.channel is not None:
            tts = gTTS(member_name + ' เข้ามา', lang='th', slow=True)
            tts.save('member.mp3')

            guild = after.channel.guild

            voice_client: discord.VoiceClient = discord.utils.get(
                bot.voice_clients, guild=guild)
            audio_source = discord.FFmpegPCMAudio('member.mp3')
            if not voice_client.is_playing():
                voice_client.play(audio_source, after=None)

        # Leaved
        if before.channel is not None and after.channel is None:
            tts = gTTS(member_name + ' ออกไป', lang='th', slow=True)
            tts.save('member.mp3')

            guild = before.channel.guild
            voice_client: discord.VoiceClient = discord.utils.get(
                bot.voice_clients, guild=guild)
            audio_source = discord.FFmpegPCMAudio('member.mp3')
            if not voice_client.is_playing():
                voice_client.play(audio_source, after=None)

        if before.channel is not None and after.channel is not None:
            if member.id == 242298671469821956 and after.self_mute is True:
                tts = gTTS('เอิร์ธปิดไมไปคุยกับผู้หญิง',
                           lang='th', slow=True)
                tts.save('member.mp3')

                guild = after.channel.guild
                voice_client: discord.VoiceClient = discord.utils.get(
                    bot.voice_clients, guild=guild)
                audio_source = discord.FFmpegPCMAudio('member.mp3')
                if not voice_client.is_playing():
                    voice_client.play(audio_source, after=None)

            if after.self_stream == True and after.self_mute == before.self_mute:
                tts = gTTS(member_name +
                           'กำลังสตรีมจอ', lang='th', slow=True)
                tts.save('member.mp3')

                guild = after.channel.guild
                voice_client: discord.VoiceClient = discord.utils.get(
                    bot.voice_clients, guild=guild)
                audio_source = discord.FFmpegPCMAudio('member.mp3')
                if not voice_client.is_playing():
                    voice_client.play(audio_source, after=None)


@bot.command()
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("ตม.เข้ามาแล้วครับ")
    else:
        await ctx.send("คุณไม่ได้อยู่ใน voice channel")


@bot.command()
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("ตม. หมดกะแล้วครับ")
    else:
        await ctx.send("ตม. เลิกงาน")


bot.run(os.getenv('TOKEN'))

import os
import discord

from discord.utils import get
from discord.ext import commands
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

        # got action
        if before.channel is not None or after.channel is not None:
            # Join
            if before.channel is None and after.channel is not None:
                if bot.voice_clients[0].channel.id == after.channel.id:
                    tts = gTTS(member_name + ' เข้ามา', lang='th', slow=True)
                    tts.save('member.mp3')

                    guild = after.channel.guild

                    voice_client: discord.VoiceClient = discord.utils.get(
                        bot.voice_clients, guild=guild)
                    audio_source = discord.FFmpegPCMAudio('member.mp3')
                    if not voice_client.is_playing():
                        voice_client.play(audio_source, after=None)

            # Leave
            if before.channel is not None and after.channel is None:
                if bot.voice_clients[0].channel.id == before.channel.id:
                    tts = gTTS(member_name + ' ออกไป', lang='th', slow=True)
                    tts.save('member.mp3')

                    guild = before.channel.guild
                    voice_client: discord.VoiceClient = discord.utils.get(
                        bot.voice_clients, guild=guild)
                    audio_source = discord.FFmpegPCMAudio('member.mp3')
                    if not voice_client.is_playing():
                        voice_client.play(audio_source, after=None)

            # move to another channel or action
            if before.channel is not None and after.channel is not None:
                if bot.voice_clients[0].channel.id == before.channel.id and after.self_mute == before.self_mute:
                    tts = gTTS(member_name + ' ออกไปห้อง' +
                               str(after.channel), lang='th', slow=True)
                    tts.save('member.mp3')

                    guild = before.channel.guild
                    voice_client: discord.VoiceClient = discord.utils.get(
                        bot.voice_clients, guild=guild)
                    audio_source = discord.FFmpegPCMAudio('member.mp3')
                    if not voice_client.is_playing():
                        voice_client.play(audio_source, after=None)

                if bot.voice_clients[0].channel.id == after.channel.id and after.self_mute == before.self_mute:
                    tts = gTTS(member_name + ' ย้ายมาจากห้อง' +
                               str(before.channel), lang='th', slow=True)
                    tts.save('member.mp3')

                    guild = after.channel.guild

                    voice_client: discord.VoiceClient = discord.utils.get(
                        bot.voice_clients, guild=guild)
                    audio_source = discord.FFmpegPCMAudio('member.mp3')
                    if not voice_client.is_playing():
                        voice_client.play(audio_source, after=None)

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
                    tts = gTTS(member_name + 'กำลังสตรีมจอ',
                               lang='th', slow=True)
                    tts.save('member.mp3')

                    guild = after.channel.guild
                    voice_client: discord.VoiceClient = discord.utils.get(
                        bot.voice_clients, guild=guild)
                    audio_source = discord.FFmpegPCMAudio('member.mp3')
                    if not voice_client.is_playing():
                        voice_client.play(audio_source, after=None)


def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


@bot.command()
async def join(ctx):
    checkBotIsConnected = is_connected(ctx)
    if checkBotIsConnected == None:
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            await ctx.send("ตม.เข้ามาแล้วครับ")
        else:
            await ctx.send("คุณไม่ได้เข้าเมือง")
    else:
        await ctx.send("ตม.เข้างานที่อื่นอยู่ครับ")


@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("ตม. หมดกะแล้วครับ")
    else:
        await ctx.send("ตม. เลิกงาน")


bot.run(os.getenv('TOKEN'))

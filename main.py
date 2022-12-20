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
        # voice channel has activity
        if before.channel is not None or after.channel is not None:
            guild = None
            tts = None
            # user join channel first time
            if before.channel is None and after.channel is not None:
                # user join same voice channel  as bot ?
                if bot.voice_clients[0].channel.id == after.channel.id:
                    tts = gTTS(member_name + ' เข้ามา', lang='th', slow=True)
                    guild = after.channel.guild
            # user leave from this server
            elif before.channel is not None and after.channel is None:
                # user leave from same channel as bot ?
                if bot.voice_clients[0].channel.id == before.channel.id:
                    tts = gTTS(member_name + ' ออกไป', lang='th', slow=True)
                    guild = before.channel.guild
            # user move the other voice channel, mute, defean, streaming
            else:
                # check user move to, move from which voice channel
                if after.self_mute == before.self_mute and after.self_deaf == before.self_deaf and after.self_stream == before.self_stream:
                    # move to same voice channel as bot
                    if bot.voice_clients[0].channel.id == after.channel.id:
                        tts = gTTS(member_name + ' ย้ายมาจากห้อง' +
                                   str(before.channel), lang='th', slow=True)
                        guild = after.channel.guild
                    elif bot.voice_clients[0].channel.id == before.channel.id:
                        tts = gTTS(member_name + ' ย้ายไปห้อง' +
                                   str(after.channel), lang='th', slow=True)
                        guild = before.channel.guild
                else:
                    # user mute, deafen or streaming on voice channel same as bot
                    if bot.voice_clients[0].channel.id == after.channel.id:
                        guild = after.channel.guild
                        if after.self_mute is True:
                            tts = gTTS(member_name + 'ปิดไม',
                                       lang='th', slow=True)
                        elif after.self_stream == True and after.self_mute == before.self_mute:
                            tts = gTTS(member_name + 'กำลังสตรีม',
                                       lang='th', slow=True)

            if guild is not None and tts is not None:
                tts.save('member.mp3')
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

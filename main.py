import os
import discord

from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from gtts import gTTS
from discord import FFmpegPCMAudio
import datetime
from datetime import timedelta
from zeep import Client
from lxml import etree
client = Client('https://orapiweb.pttor.com/oilservice/OilPrice.asmx?WSDL')

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='#', intents=intents)


def isBot(m):
    return m.author == bot.user


def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


def getOilPrice():

    embed = discord.Embed(title="ราคาน้ำมันจาก ปตท.",
                          colour=discord.Colour.random())
    embed.set_author(name=f"{bot.user}")
    embed.set_thumbnail(url=f"{bot.user.display_avatar}")
    # datenow
    dateNow = str(datetime.date.today())
    dn = dateNow.split("-")
    result = client.service.GetOilPrice("en", dn[2], dn[1], dn[0])
    root = etree.fromstring(result)
    embed.add_field(name="ราคาน้ำมันวันที่ ",
                    value=f"{str(dateNow)}", inline=False)
    for r in root.xpath('FUEL'):
        product = r.xpath('PRODUCT/text()')[0]
        price = r.xpath('PRICE/text()') or [0]
        price = str(price).translate({ord(i): None for i in "'[]"})
        embed.add_field(name=f"{str(product)}",
                        value=f"{str(price)} บาท", inline=True)

    # tomorrow
    tomorrow = str(datetime.date.today()+timedelta(1))
    tm = tomorrow.split("-")
    result2 = client.service.GetOilPrice("en", tm[2], tm[1], tm[0])
    root2 = etree.fromstring(result2)
    embed.add_field(name="ราคาน้ำมันวันที่ ",
                    value=f"{str(tomorrow)}", inline=False)
    for r in root2.xpath('FUEL'):
        product = r.xpath('PRODUCT/text()')[0]
        price = r.xpath('PRICE/text()') or [0]
        price = str(price).translate({ord(i): None for i in "'[]"})
        embed.add_field(name=f"{str(product)}",
                        value=f"{str(price)} บาท", inline=True)

    return embed


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
                        if after.self_mute is True and after.self_stream == before.self_stream:
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


@bot.command()
async def clear(ctx):
    await ctx.channel.purge(limit=100, check=isBot)


@bot.command()
async def fuel(ctx):
    result_embed = getOilPrice()
    await ctx.send(embed=result_embed)

bot.run(os.getenv('TOKEN'))

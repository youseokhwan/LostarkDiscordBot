import asyncio, discord
from check import *

bot = discord.Client()

@bot.event
async def on_ready():
    print("로그인: {0.user}".format(bot))
    await bot.change_presence(activity = discord.Game(name = "LOST ARK"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content

    if msg[0] != "!":
        return

    if len(msg) < 2:
        return

    username = msg[1:]

    className, contents, color = getData(username)
    embed = discord.Embed(title = username + "(" + className + ")", description = contents, color = color)
    embed.set_footer(text = "발탄[노말] 기준")
    await message.channel.send(embed = embed)

bot.run("private token")

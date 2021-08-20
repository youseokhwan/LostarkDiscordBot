import asyncio, discord
from check import *
from criterion import *

bot = discord.Client()
key = "비아하드"

def setCriteria(criteria):
    if criteria in criterion:
        global key
        key = criteria
        return True
    else:
        return False

@bot.event
async def on_ready():
    print("로그인: {0.user}".format(bot))
    await bot.change_presence(activity = discord.Game(name = "LOST ARK"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content

    if msg[0] != "!" or msg == "!" or msg.find(" ") != -1:
        return

    if msg == "!!":
        await message.channel.send(printHelp())
        return

    if msg == "!!!":
        await message.channel.send(printCriterion())
        return

    if msg.startswith("!!+"):
        await message.channel.send(addCriterion(msg))
        return

    if msg.startswith("!!="):
        await message.channel.send(updateCriterion(msg))
        return

    if msg.startswith("!!-"):
        await message.channel.send(deleteCritirion(msg))
        return

    if msg.startswith("!!"):
        criteria = msg[2:]
        if setCriteria(criteria):
            await message.channel.send("기준이 `" + criteria + "`로 설정되었습니다.")
        else:
            await message.channel.send("설정 가능한 기준이 아닙니다. `!!` 명령어로 목록을 확인해주세요.")
        return

    username = msg[1:]

    className, contents, color = getData(username, key)
    embed = discord.Embed(title = username + "(" + className + ")", description = contents, color = color)
    embed.set_footer(text = key + " 기준")
    await message.channel.send(embed = embed)

bot.run("your token")

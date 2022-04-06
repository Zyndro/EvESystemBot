import requests
import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
wpierdol = ["R1O-GN", "LXQ2-T", "4-HWWF", "T5ZI-S", "Y-MPWL", "PR-8CA", "J-ZYSZ", "D-PNP9", "G-M4GK", "UGR-J2",
            "MJ-5F9", "Q-5211"]
jita = ["Jita"]


def systemsEVE(sysname):
    connectionlist = []
    try:
        for destynacjax in sysname:
            url = 'https://www.eve-scout.com/api/wormholes?systemSearch=' + destynacjax + '&method=shortest&limit=1000&offset=0&sort=jumps&order=asc'
            r = requests.get(url, headers={'accept': 'application/json'})
            connectionlisttemp = []
            for x in r.json():
                jmp = x['jumps']
                name = x['destinationSolarSystem']['name']
                sig = x['signatureId']
                reg = x['destinationSolarSystem']['region']['name']
                eol = x['wormholeEol']
                if 0 < jmp < 14:
                    connectionlisttemp.append(
                        f' {destynacjax} \n sygnatura: {sig} \n ile: {jmp} \n wlotowy: {name} \n region: {reg} \n EoL: {eol}')
            if not connectionlisttemp:
                connectionlist.append((f'{destynacjax} za daleko albo nima'))
            if connectionlisttemp:
                for x in connectionlisttemp:
                    connectionlist.append(x)

        return connectionlist
    except Exception as e:
        return e


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$systemy'):
        await message.channel.send("Szukam...")
        for x in systemsEVE(wpierdol):
            await message.channel.send("```yaml\n" + x + "```")
        await message.channel.send("Znalazłem!")

    if message.content.startswith('$jita'):
        for x in systemsEVE(jita):
            await message.channel.send("```yaml\n" + x + "```")

    if message.content.startswith('$help'):
        await message.channel.send("```yaml\n" + "Komendy: \n $jita \n $systemy" + "```")


client.run(TOKEN)

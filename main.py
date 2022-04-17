import requests
import discord
import os
from PIL import Image,ImageFont, ImageDraw
from dotenv import load_dotenv
import re

load_dotenv()
TOKEN = os.getenv("TOKEN")
myFont = ImageFont.truetype('arial.ttf', 30)
wpierdol = ["R1O-GN", "LXQ2-T", "4-HWWF", "T5ZI-S", "Y-MPWL", "PR-8CA", "J-ZYSZ", "D-PNP9", "G-M4GK", "UGR-J2",
            "MJ-5F9", "Q-5211"]
jita = ["Jita"]
amarr = ["Amarr"]
hek = ["Hek"]
rens = ["Rens"]

def systemsEVE(sysname):
    connectionlist = []
    try:
        lastjump = 0
        for destynacjax in sysname:
            url = 'https://www.eve-scout.com/api/wormholes?systemSearch=' + destynacjax + '&method=shortest&limit=1000&offset=0&sort=jumps&order=asc'
            r = requests.get(url, headers={'accept': 'application/json'})
            for x in r.json():
                jmp = x['jumps']
                name = x['destinationSolarSystem']['name']
                sig = x['signatureId']
                reg = x['destinationSolarSystem']['region']['name']
                eol = x['wormholeEol']
                source = x['sourceWormholeType']['dest']
                if 0 < jmp < 14:
                        connectionlist.append(
                            f' {destynacjax} | sygnatura: {sig} | ile: {jmp} | wlotowy: {name}({source}) | region: {reg} | EoL: {eol}')
        connectionlist = sorted(connectionlist, key=ile_sort)
        return connectionlist
    except Exception as e:
        connectionlist.append(str(e))
        return connectionlist

def ile_sort(elem):
    return int(re.findall('ile: (\d+)', elem)[0])

def draw_list(h,w,list):
    img = Image.new("RGB", (h, w), (0, 0, 0))
    I1 = ImageDraw.Draw(img)
    line = 0
    for x in list:
        I1.text((10, (line + 40)), x, font=myFont, fill=(255, 255, 255))
        shape = [(10, 40 + line), (h - 10, 40 + line)]
        I1.line(shape, fill=128, width=7)
        line = line + 40
    shape = [(10, 40 + line), (h - 10, 40 + line)]
    I1.line(shape, fill=128, width=8)
    img.save("systemy.png")
    return "systemy.png"


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
        listasystemow = systemsEVE(wpierdol)
        img = draw_list((len(max(listasystemow, key=len))*14),((len(listasystemow)*45)+45),listasystemow)
        await message.channel.send(file=discord.File(img))
        await message.channel.send("Znalazłem!")
        os.remove(img)

    if message.content.startswith('$jita'):
        for x in systemsEVE(jita):
            await message.channel.send("```yaml\n" + x + "```")

    if message.content.startswith('$amarr'):
        for x in systemsEVE(amarr):
            await message.channel.send("```yaml\n" + x + "```")

    if message.content.startswith('$hek'):
        for x in systemsEVE(hek):
            await message.channel.send("```yaml\n" + x + "```")

    if message.content.startswith('$rens'):
        for x in systemsEVE(rens):
            await message.channel.send("```yaml\n" + x + "```")

    if message.content.startswith('$help'):
        await message.channel.send("```yaml\n" + "Komendy: \n $jita \n $amarr \n $hek \n $rens \n $systemy" + "```")


client.run(TOKEN)

import requests
import discord
import os
from PIL import Image, ImageFont, ImageDraw
from dotenv import load_dotenv
import re

load_dotenv()
TOKEN = os.getenv("TOKEN")
interest_systems = ["R1O-GN", "LXQ2-T", "4-HWWF", "T5ZI-S", "Y-MPWL", "PR-8CA", "J-ZYSZ", "D-PNP9", "G-M4GK", "UGR-J2", "MJ-5F9", "Q-5211"]
jita = ["Jita"]
amarr = ["Amarr"]
hek = ["Hek"]
rens = ["Rens"]


def systems_eve(sysname):
    connection_list = []
    try:
        for destination in sysname:
            url = 'https://www.eve-scout.com/api/wormholes?systemSearch=' + destination + '&method=shortest&limit=1000&offset=0&sort=jumps&order=asc'
            r = requests.get(url, headers={'accept': 'application/json'})
            for x in r.json():
                jmp = x['jumps']
                name = x['destinationSolarSystem']['name']
                sig = x['signatureId']
                reg = x['destinationSolarSystem']['region']['name']
                eol = x['wormholeEol']
                source = x['sourceWormholeType']['dest']
                # maximum distance of 13 jumps
                if 0 < jmp < 14:
                    connection_list.append(
                        f' {destination} | sygnatura: {sig} | ile: {jmp} | wlotowy: {name}({source}) | region: {reg} | EoL: {eol}')
        connection_list = sorted(connection_list, key=ile_sort)
        return connection_list
    except Exception as e:
        connection_list.append(str(e))
        return connection_list


def ile_sort(elem):
    return int(re.findall('ile: (\d+)', elem)[0])


# width and height may be actually switched incorrectly
def draw_list(h, w, lista):
    image_font = ImageFont.truetype('arial.ttf', 30)
    img = Image.new("RGB", (h, w), (0, 0, 0))
    drawing = ImageDraw.Draw(img)
    line = 0
    for x in lista:
        drawing.text((10, (line + 40)), x, font=image_font, fill=(255, 255, 255))
        shape = [(10, 40 + line), (h - 10, 40 + line)]
        drawing.line(shape, fill=128, width=7)
        line = line + 40
    shape = [(10, 40 + line), (h - 10, 40 + line)]
    drawing.line(shape, fill=128, width=8)
    img.save("systems.png")
    return "systems.png"


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
        lista_systemow = systems_eve(interest_systems)
        img = draw_list((len(max(lista_systemow, key=len)) * 14), ((len(lista_systemow) * 45) + 45), lista_systemow)
        await message.channel.send(file=discord.File(img))
        await message.channel.send("Znalazłem!")
        os.remove(img)

    if message.content.startswith('$jita'):
        for x in systems_eve(jita):
            await message.channel.send("```yaml\n" + x + "```")

    if message.content.startswith('$amarr'):
        for x in systems_eve(amarr):
            await message.channel.send("```yaml\n" + x + "```")

    if message.content.startswith('$hek'):
        for x in systems_eve(hek):
            await message.channel.send("```yaml\n" + x + "```")

    if message.content.startswith('$rens'):
        for x in systems_eve(rens):
            await message.channel.send("```yaml\n" + x + "```")

    if message.content.startswith('$help'):
        await message.channel.send("```yaml\n" + "Komendy: \n $jita \n $amarr \n $hek \n $rens \n $systemy" + "```")

    # draw test
    if message.content.startswith('$test'):
        lista = [' LXQ2-T | ile: 6 |', ' UGR-J2 | ile: 8 |', ' LXQ2-T | ile: 9 |']
        dimensions = re.findall(r'\b\d+\b', message.content)
        try:
            img = draw_list(int(dimensions[0]), int(dimensions[1]), lista)
            await message.channel.send(file=discord.File(img))
            os.remove(img)
        except IndexError:
            await message.channel.send("Provide correct image dimensions! \n i.e. ***$test 200 300***")

if __name__ == "__main__":
    client.run(TOKEN)

# bot.py
import os
from datetime import datetime

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from Bot import eventTimer

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')


client = CustomClient()


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == '!se':
        response = eventTimer.timeUntilSpecificEvent()
        await message.channel.send(response)

    if message.content.lower() == '!events':
        response = eventTimer.returnEventOptions()
        await message.channel.send(response)

    if message.content.lower() == '!jerry' or message.content.lower() == '!soj' or message.content.lower() == '!christmas':
        response = eventTimer.timeUntilSpecificEvent('Season of Jerry')
        await message.channel.send(response)

    if message.content.lower() == '!newyear' or message.content.lower() == '!nyc' or message.content.lower() == 'new year' \
            or message.content.lower() == '!cake':
        response = eventTimer.timeUntilSpecificEvent('New Year Celebration')
        await message.channel.send(response)
    if message.content.lower() == 'is logan cool?':
        response = 'Yeah, that dude is awesome!'
        await message.channel.send(response)
    if message.content.lower() == 'are you gay':
        response = "Nah, I ain't gay homie."
        print(message.author)
        await message.channel.send(response)

async def eventStart():
    if True == True:
        print('test')
        member = discord.member()
        member.create_dm()
        member.dm_channel.send('YO')


async def dm():

    user=client.get_user_info("Loganphx#1991")
    print(user)
    #await client.send_message(user, "Your message goes here")

client.run(TOKEN)

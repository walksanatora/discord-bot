# bot.py
import os
import random

import discord
from dotenv import load_dotenv
#defining of variables

#load .env as enviroment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PREFIX = os.getenv('PREFIX')
BOT_CHANNEL = int(os.getenv('BOT_CHANNEL'))
BOT_ID = os.getenv('BOT_ID')
#init the bot
client = discord.Client()

#ease of use
space = ' '
mention = f'<@!{BOT_ID}>'

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(f'mention is: {mention}')
    print(
        f'{client.user} is connected to the following server:\n'
        f'{guild.name} with id: {guild.id}\n'
        f'bot prefix is: {PREFIX}\n'
        f'bot is bound to channel id: {BOT_CHANNEL}\n'
        f'the bot @ is: <@!{client.user.id}>'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id == BOT_CHANNEL : #make shure the bot is being used in the bot channel
        print(f'message \"{message.content}\" was sent in server \"{message.guild}\" specifically in #{message.channel}') #log all chat happening in #bots
        command=f'{message.content}'
        command=command.split(' ')
        print(f'{command} is type {type(command)}')
        if command[0] == PREFIX + '?': #help command
            embed = discord.Embed(title="Command help",description="command",color=0x00ffaa)
            embed.add_field(name='?',value=f'use {PREFIX}? to get help',inline=False)
            embed.add_field(name='disable',value=f'use {PREFIX}disable to disconnect the bot and turn it off',inline=False)
            embed.add_field(name='repeat [text to say]',value=f'use {PREFIX}repeat to have the bot say stuff',inline=False)
            await message.channel.send(embed=embed)
        elif command[0] == PREFIX + 'raise-exception': #cause an intentional error
            print('exception manually raised')
            raise discord.DiscordException
        elif command[0] == PREFIX + 'disable': #bot is kil
            print('going offline')
            await message.channel.send('shutting down the bot')
            await client.change_presence(status=discord.Status.offline)
            print('exiting')
            await client.close()
            quit()
        elif command[0] == PREFIX + 'repeat':
            command.pop(0)
            command = space.join(command)
            await message.channel.send(command)
        elif command[0] == PREFIX + 'audio':
            print('rick rolling')
            user=message.author
            print('user obtained')
            voice_channel = client.get_channel(783738781538844697)
            print(f'channel obtained {voice_channel}')
            await voice_chat.join()
            print('connected to vc')
            player = await voice_chat.join().create_ffmpeg_player('audio.mp3')
            print('audio is ready')
            await player.start()
            print('never gonna give you up')
        elif command[0] == "<@596098777941540883>":
            print(f'who tf pinged walksanator')
            await message.channel.send(
                f'someone pinged walksanator\n'
                f'it was <@{message.author}>\n'
                f'(you deverve the ping :ping-pong: )'
            )
        elif command[0] == mention: #bot was pinged so lets give the prefix
            print(f'pinged')
            await message.channel.send(
                f'I have been pinged, \n'
                f'Here is the prefix: {PREFIX} \n'
                f'use {PREFIX}? to get help \n'
            )
#    else:

        
    

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
        
client.run(TOKEN)

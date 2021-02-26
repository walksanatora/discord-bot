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
try:
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
except Exception as err:
    print('massive fuck up trying to correct logging to log.txt')
    with open('err.log', 'a') as f:
        f.write(f'(init) massive fuckup hereis the log sir: {err}')
try:
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id == BOT_CHANNEL : #make shure the bot is being used in the bot channel
        print(f'message \"{message.content}\" was sent in server \"{message.guild}\" specifically in #{message.channel}') #log all chat happening in #bots
        command=f'{message.content}'
        command=command.split(' ')
        print(f'command array is {command}')
        print(f'{command} is type {type(command)}')
        if command[0] == PREFIX + '?': #help command
            embed = discord.Embed(title="Command help",description="command",color=0x00ffaa)
            embed.add_field(name='?',value=f'use {PREFIX}? to get help',inline=False)
            embed.add_field(name='disable',value=f'use {PREFIX}disable to disconnect the bot and turn it off',inline=False)
            embed.add_field(name='repeat [text to say]',value=f'use {PREFIX}repeat to have the bot say stuff',inline=False)
            embed.add_field(name='search',value=f'use {PREFIX}search(channel id, user id) to search entire channel for messages by specified user id',inline=False)
            embed.add_field(name='test',value=f'use {PREFIX}test to run a test command',inline=False)
            await message.channel.send(embed=embed)
        elif command[0] == PREFIX + 'test':
            await message.channel.send('test command invoked this whould appear after rebooting the pi ;-; hopefully')
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
#        elif command[0] == PREFIX + 'audio': #this is broken
#            print('rick rolling')
#           user=message.author
#            print('user obtained')
#            voice_channel = client.get_channel(783738781538844697)
#            print(f'channel obtained {voice_channel}')
#            await voice_chat.join()
#            print('connected to vc')
#            player = await voice_chat.join().create_ffmpeg_player('audio.mp3')
#            print('audio is ready')
#            await player.start()
#            print('never gonna give you up')
        elif command[0] == PREFIX + "search":
            embed = discord.Embed(title="Command help",description="command",color=0x00ffaa)
            ittr = 0
            #print(f'searching {command[1]} for messages by <@{command[2]}>')
            channel = message.guild.get_channel(int(command[1]))
            messages = await channel.history(limit=None).flatten()
            print(f'len messages {len(messages)}')
            for msgs in messages:
                #print(f'message author id is {msgs.author.id} it needs to be {int(command[2])} ')
                ittr=ittr+1
                print(f'itteration {ittr}')
                if msgs.author.id == int(command[2]):
                    #print (f'{msgs.id} was sent by {command[2]} in {channel.name}')
                    embed.add_field(name='disable',value=f'message {msgs.id} was sent by specified user in the specified channel',inline=False)            
            print('search finished')
            await message.channel.send(embed=embed)
            print('search finished')
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
except Exception as err:
    print('massive fuck up trying to correct logging to log.txt')
    with open('err.log', 'a') as f:
        f.write(f'(commands)massive fuckup here is the log sir: {err}')
        
    

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
        
client.run(TOKEN)

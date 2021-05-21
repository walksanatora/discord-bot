#loading of modules
import os
import time
import discord
from discord.ext import tasks
import NSrefactor as NS
from dotenv import load_dotenv
import database
import xml.etree.ElementTree as ET
import commands
import traceback
DB=database.db('db.json')
LOG=database.db('logging.json')
import logs
import traceback

#defining globals
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX=os.getenv('PREFIX')
#os.environ['CONSOLE']=str(True)
CONSOLE=bool(os.getenv('CONSOLE'))

#init the bot api
client = discord.Client()



#non-bot functions


#bot functions that make the bot work
@client.event
async def on_ready():
    logs.log(f'bot is online as " {client.user} "')


@tasks.loop(hours=6.0)
async def reGenKey():
    try:
        global NSA
        NSA=NS.api(False,os.getenv('NS_NATION'),os.getenv('NS_PASSWORD'))
        logs.log('re-loaded api')
    except Exception:
        logs.log("ohnoes something went wwong 【ᵔ̃ ⏥ᵔ̃ 】")
        traceback.logs.log_exc()
reGenKey.start()

@client.event
async def on_message(message):
    try:
        command = str.split(message.content,' ')
        cmd = commands.commands
        if not command[0].startswith(PREFIX):
            return
        command[0]=command[0][1:]
        logs.log(command)
        try:
            await getattr(cmd,command[0]).run(message,NSA,command)
        except AttributeError:
            logs.log('attrib ohno',traceback.format_exc())
            pass
    except NSA.exception.httpError as error:
        await message.channel.send(content='a http error has occured try again in a little bit')
        logs.log(error)
    except Exception as error:
        logs.log('a big error occured')
        logs.log(error)
        logs.log(traceback.format_exc())
if not CONSOLE:
    client.run(TOKEN)
    logs.log('post run')

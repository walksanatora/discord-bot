#loading of modules
import os
import re
import time
import discord
import NSrefactor as NS
from dotenv import load_dotenv
import database
import xml.etree.ElementTree as ET
DB=database.db('db.json')
LOG=database.db('logging.json')


#defining globals
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX='?'
#os.environ['CONSOLE']=str(True)
CONSOLE=bool(os.getenv('CONSOLE'))

#init the bot api
client = discord.Client()

#nation states api
NSA=NS.api(os.getenv('NS_PASSWORD'), os.getenv('NS_NATION'), os.getenv('USER_AGENT'))

#non-bot functions
def cleanHtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

async def recursiveReply(channel,reference, count):
    print(channel, type(reference), count)
    if str(type(reference)) == "<class 'NoneType'>":
        return count
    else:
        ref = await channel.fetch_message(reference.message_id)
        return(await recursiveReply(channel, ref.reference, count+1))

def submitIssueVotes():
    for f in DB.data:
        id=f
        votes = {}
        for k, v in f.items():
            if int(v) <= 6:
                try:
                    votes[str(v)] = int(votes[str(v)]) + 1
                except Exception as e:
                    votes[str(v)] = 1
        win = [0,0]
        for k, v in votes.items():
            if int(v) > win[1]:
                win = [int(k), int(v)]
        if not type(LOG.data[str(id)]) == type([]):
            LOG.data[str(id)]=[]
        LOG.data[str(id)].append(NSA.functions.submitIssue(id, win[0])[1])
        del(DB.data[str(id)])
        DB.saveDB()
        log.saveDB()
        time.sleep(1)

#bot functions that make the bot work
@client.event
async def on_ready():
    print(f'bot is online as " {client.user} "')

@client.event
async def on_message(message):
    try:
        if CONSOLE:
            command = message.split(' ')
        else:
            command=f'{message.content}'
            command=command.split(' ')
        if command[0] == f'{PREFIX}issues':
            issues = NSA.functions.getIssues()
            embed = discord.Embed(title='issues facing the nation',description='current issues the nation is facing',color=0x800000)
            if not CONSOLE:
                for i in issues:
                    embed.add_field(name=f'{i.title}**\nID:**{i.id}',value=cleanHtml(i.background),inline=False)
                await message.channel.send(embed=embed)
            else:
                for i in issues:
                    print(f'issue:\n'
                        f'\t{i.title}\n'
                        f'\tInformation:{cleanHtml(i.background)}\n'
                        f'\t\n'
                        f'\tOptions:')
                    for a in i.options:
                        print(f'\t\t{a}\n')
                    input('press enter to continue:')
                return(issues)
        if command[0] == f'{PREFIX}newIssue':
            nextIssue = NSA.functions.getTimeTillNextIssue()
            embed = discord.Embed(Title='time remeaning till next issue',description='how much longer till the next issue becomes avaliable')
            embed.add_field(name='time remaning',value=f'{nextIssue[0]}',inline=True)
            if not CONSOLE:
                await message.channel.send(embed=embed)
            else:
                print(embed)

        if command[0] == f'{PREFIX}vote':
            if not NSA.functions.validateIssueID(command[1]):
                if not CONSOLE:
                    await message.channel.send(content='not a valid issue to vote on')
                else:
                    print('not a valid issue to vote on')
                return
            if not command[1] in DB.data:
                DB.data[command[1]] = {}
            DB.data[command[1]][str(message.author.id)] = str(command[2])
            DB.saveDB()

        if command[0] == f'{PREFIX}submit':
            if CONSOLE:
                if message.channel.permissions_for(message.author).administrator or message.author.id==int('596098777941540883'):
                    message.channel.send(content='submitting votes')
                    submitIssueVotes()
            else:
                print('submitting votes')
                submitIssueVotes()
        if command[0] == f'{PREFIX}replyChain' and not CONSOLE:
            ref = await message.channel.fetch_message(int(command[1]))
            await message.channel.send(content=f'this message is a part of a reply chain {await recursiveReply(message.channel,  ref.reference, 1)} messages long')
    except NSA.exception.httpError as error:
        await message.channel.send(content='a http error has occured try again in a little bit')

if not CONSOLE:
    client.run(TOKEN)
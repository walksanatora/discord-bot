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
NSA=NS.api(False,os.getenv('NS_NATION'),os.getenv('NS_PASSWORD'))

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
    for index in DB.data:
        _id=index
        votes = {}

        #get a list of votes for each id
        for userID, vote in DB.data[_id].items():
            if int(vote) <= 6:
                try:
                    votes[str(vote)] = int(votes[str(vote)]) + 1
                except Exception as e:
                    votes[str(vote)] = 1

        #compare votes to see which has more votes and the id
        win = [0,0]
        for vote, ammount in votes.items():
            if int(ammount) > win[1]:
                win = [int(vote), int(ammount)]

        #log the votes and send off the results
        try:
            if not type(LOG.data[str(_id)]) == type([1,2,3]):
                LOG.data[str(_id)]=[]
        except KeyError as e:
            LOG.data[str(_id)]=[]
        LOG.data[str(_id)].append(str(NSA.functions.submitIssue(_id, win[0]).text))
        time.sleep(1)

    #delete the data from the db
    DB.data={}
    
    #save the databases
    DB.saveDB()
    LOG.saveDB()
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
        if not CONSOLE and command[0]==client.user.id or command[0]==f'{PREFIX}help':
            embed = discord.Embed(title=f'Help bot commands prefix: {PREFIX}',description='here are the (documented) commands',color=0x00ffaa)
            embed.add_field(name=f'{PREFIX}help',value='shows this message')
            embed.add_field(name=f'{PREFIX}issues',value='shows all the issues the nation is facing')
            embed.add_field(name=f'{PREFIX}newIssue',value='shows time till next issue')
            embed.add_field(name=f'{PREFIX}vote',value='submit your vote upon a issue')
            embed.add_field(name=f'{PREFIX}submit',value='(admin only) submits the votes on all issues')
            embed.add_field(name=f'{PREFIX}replyChain',value='gets the lenght of a reply chain(may take a bit)')
            await message.channel.send(embed=embed)
        if command[0] == f'{PREFIX}issues':
            issues = NSA.functions.getIssues()
            embed = discord.Embed(title='Issues Facing The Nation',description='current issues the nation is facing',color=0x800000)
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
        if command[0] == f'{PREFIX}issueOptions':
            issues = NSA.functions.getIssues()
            for issue in issues:
                if issue.id == command[1]:
                    print('issue found')
                    embed=discord.Embed(title=f'{issue.title} id:{command[1]}',description=issue.background)
                    cout=1
                    for f in issue.options:
                        embed.add_field(name=f'option:{cout}',value=f,inline=False)
                        cout=cout+1
                    await message.channel.send(embed=embed)
                    break
        if command[0] == f'{PREFIX}newIssue':
            nextIssue = NSA.functions.getTimeTillNextIssue()
            embed = discord.Embed(Title='Time Remeaning Till Next Issue',description='how much longer till the next issue becomes avaliable')
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
            await message.channel.send('vote collected')

        if command[0] == f'{PREFIX}submit':
            print('submitting')
            if not CONSOLE:
                if message.channel.permissions_for(message.author).administrator or message.author.id==int('596098777941540883'):
                    msg = await message.channel.send(content='submitting votes')
                    submitIssueVotes()
                    await msg.edit(content='votes submitted')
            else:
                print('submitting votes')
                submitIssueVotes()
        if command[0] == f'{PREFIX}replyChain' and not CONSOLE:
            ref = await message.channel.fetch_message(int(command[1]))
            await message.channel.send(content=f'this message is a part of a reply chain {await recursiveReply(message.channel,  ref.reference, 1)} messages long')
    except NSA.exception.httpError as error:
        await message.channel.send(content='a http error has occured try again in a little bit')
        print(error)

if not CONSOLE:
    client.run(TOKEN)
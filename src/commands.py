import discord
from dotenv import load_dotenv
import re
load_dotenv()
import os
PREFIX=os.getenv('PREFIX')
import database
DB=database.db('db.json')
LOG=database.db('logging.json')
import logs

def submitIssueVotes():
    try:
        for index in DB.data:
            _id=index
            votes = {}
            logs.log(f'type:{type(DB.data[_id])} id:{_id} data:{DB.data[_id]}')
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
            LOG.data[str(_id)].append(str(NSA.functions.submitIssue(_id, win[0])[0].text))
            time.sleep(1)

        #delete the data from the db
        DB.data={}

        #save the databases
        DB.saveDB()
        LOG.saveDB()
    except Exception as e:
        with open('log.txt','a') as f:
            f.write(f'{e}')
            raise

def cleanHtml(raw_html):

  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

async def recursiveReply(channel,reference, count):
    logs.log(channel, type(reference), count)
    if str(type(reference)) == "<class 'NoneType'>":
        return count
    else:
        ref = await channel.fetch_message(reference.message_id)
        return(await recursiveReply(channel, ref.reference, count+1))

class commands:
    class help:
        async def run(message,NSA,command):
            embed = discord.Embed(title=f'Help bot commands prefix: {PREFIX}',description='here are the commands from this bot',color=0x00ffaa)
            for name in dir(commands):
                if not name.startswith('_'):
                    attr = getattr(commands, name)
                    if isinstance(attr, type(commands)):
                        if not attr.isHidden:
                            embed.add_field(name=f'{PREFIX}{name}',value=f'{attr.helpText}')
            await message.channel.send(embed=embed)

        helpText = 'this is the help command, do not judge'
        isHidden = False
        
    class issues:
        async def run(message,NSA,command):
            issues = NSA.functions.getIssues()
            embed = discord.Embed(title='Issues Facing The Nation',description='current issues the nation is facing',color=0x800000)
            for i in issues:
                embed.add_field(name=f'{i.title}**\nID:**{i.id}',value=cleanHtml(i.background),inline=False)
            await message.channel.send(embed=embed)
        helpText='shows all the issues the nation is facing'
        isHidden = False
    
    class issueOptions:
        async def run(message,NSA,command):
            issues = NSA.functions.getIssues()
            for issue in issues:
                if issue.id == command[1]:
                    logs.log('issue found')
                    embed=discord.Embed(title=f'{issue.title} id:{command[1]}',description=issue.background)
                    cout=1
                    for f in issue.options:
                        embed.add_field(name=f'option:{cout}',value=f,inline=False)
                        cout=cout+1
                    await message.channel.send(embed=embed)
                    break
        helpText='list the options avaliable for a given issue'
        isHidden = False
    
    class newIssue:
        async def run(message,NSA,command):
            nextIssue = NSA.functions.getTimeTillNextIssue()
            embed = discord.Embed(Title='Time Remeaning Till Next Issue',description='how much longer till the next issue becomes avaliable')
            embed.add_field(name='time remaning',value=f'{nextIssue[0]}',inline=True)
            await message.channel.send(embed=embed)

        helpText='shows time till next issue'
        isHidden = False

    class vote:
        async def run(message,NSA,command):
            if not NSA.functions.validateIssueID(command[1]):
                await message.channel.send(content='not a valid issue to vote on')
                return
            if not command[1] in DB.data:
                DB.data[command[1]] = {}
            DB.data[command[1]][str(message.author.id)] = str(command[2])
            DB.saveDB()
            await message.channel.send(content='vote collected')
        helpText='submit your vote upon a issue'
        isHidden = False

    class submit:
        async def run(message,NSA,command):
            if message.channel.permissions_for(message.author).administrator or message.author.id==int('596098777941540883'):
                msg = await message.channel.send(content='submitting votes')
                submitIssueVotes()
                await msg.edit(content='votes submitted')
        helpText='(admin only) submits the votes on all issues'
        isHidden = False

    class replyChain:
        async def run(message,NSA,command):
            ref = await message.channel.fetch_message(int(command[1]))
            await message.channel.send(content=f'this message is a part of a reply chain {await recursiveReply(message.channel,  ref.reference, 1)} messages long')
        helpText='gets the lenght of a reply chain(may take a bit)'
        isHidden = False

    class generic:
        async def run(message,NSA,command):
            await message.channel.send(content=command)
        helpText='this is a example command'
        isHidden = True

    class nation:
        async def run(message,NSA,command):
            await message.channel.send(content=f'https://www.nationstates.net/nation={os.getenv("NS_NATION")}')
        helpText='links the nation this bot is connected to'
        isHidden = False

    class rr:
        async def run(message,NSA,command):
            voice_channel = message.guild.get_channel(int(command[1]))
            logs.log(voice_channel)
            channel = None
            if voice_channel != None:
                channel = voice_channel.name
                logs.log(channel)
                vc = await voice_channel.connect()
                logs.log('connected to vc',vc)
                vc.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffpmeg", source="/discord-bot/audio/rickRoll.mp3"))
                # Sleep while audio is playing.
                while vc.is_playing():
                    sleep(.1)
                await vc.disconnect()
            else:
                await message.channel.send(content="wait this is not a channel")
            # Delete command after the audio is done playing.
        helpText='rickrolls you if you are in a vc'
        isHidden=False
    
    class eval:
        async def run(message,NSA,command):
            command=command[1:]
            logs.log(' '.join(command))
            logs.log(exec(' '.join(command)))
        helpText='no'
        isHidden=True

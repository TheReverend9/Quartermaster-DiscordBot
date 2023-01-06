  #!/usr/bin/env python

'''
Created on Aug 6, 2022
Updated: January 5, 2022

@author: Reverend Studios
'''
#Quartermaster bot for Discord
#Performs multiple functions to help with the daily hassles of running a discord server.


#BOT VERSION
version = '2.0'
patches='Version' + version + '.txt'

import asyncio
import discord
import json
import os
from dotenv import load_dotenv
from datetime import date
from discord.ext import commands




#filename initialization
month = date.today()
month = month.strftime('%m')
filename = 'Server List.json'
currentFile = 'Current Event.json'

load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")
GUILD=os.getenv("DISCORD_GUILD")
GENERAL=os.getenv('GENERAL')
Creator=os.getenv('Creator')
Channel0,Channel1,Channel2,Channel3,Channel4, Channel5=os.getenv('Channel0'),os.getenv('Channel1'),os.getenv('Channel2'),os.getenv('Channel3'),os.getenv('Channel4'),os.getenv('Channel5')
Role0,Role1,Role2,Role3,Role4,Role5=os.getenv('Role0'),os.getenv('Role1'),os.getenv('Role2'),os.getenv('Role3'),os.getenv('Role4'),os.getenv('Role5')
User0,User1,User2=os.getenv('User0'),os.getenv('User1'),os.getenv('User2')


intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

try:
    with open(filename, "r") as file:
        eventID = json.load(file)
except:
    print(f'ERROR: No ({filename}) file found')
try:
    with open('user roles.json', "r") as file:
        userRole = json.load(file)
except:
    print('ERROR: No (user roles.json) file found')
bot = commands.Bot(case_insensitive=True)
            
#Used to get user ID for event(eventID to be used in future update)            
@bot.event
async def on_raw_reaction_add(payload):
    event = []
    eventID = []
    userRole = []
    try:
        with open(currentFile, "r") as file:
            eventID = json.load(file)
    except Exception as e:
        print(e)
    try:
        with open('user roles.json', "r") as file:
            userRole = json.load(file)
    except Exception as e:
        print(e)

    day = date.today()
    day = day.strftime('%m')
    channel = payload.channel_id
    guild = bot.get_guild(int(payload.guild_id))

    userID = payload.user_id
    user = await bot.fetch_user(userID)
    user = str(user)

    xboxRole = discord.utils.get(guild.roles, name='XBOX')
    pcRole = discord.utils.get(guild.roles, name='PC')
    
    
    if str(channel) == GENERAL:
        userID = '<@' + str(userID) + '>'
        user = '<' + day + '>' + str(user)
        eventID.append(user)
        
        try:
            with open(currentFile, "w") as file:
                json.dump(eventID, file, indent=2)
        except Exception as e:
            print(e)

        if xboxRole in payload.member.roles:
            
            userIDrole = [userID, 'XBOX']
            userRole.append(userIDrole)
           
            
        elif pcRole in payload.member.roles:
            userIDrole = [userID, 'PC']
            userRole.append(userIDrole)
            
        else:
            userIDrole = [userID, 'UNDEF']
            userRole.append(userIDrole)
        
        try:
            with open('user roles.json', "w") as file:
                json.dump(userRole, file, indent=2)
        except:
            print('ERROR: Unable to save user roles to (user roles.json)')
        
                
#on_raw_reaction_remove deletes user from event list   
@bot.event
async def on_raw_reaction_remove(payload):
    day = date.today()
    day = day.strftime('%m')
    channel = payload.channel_id
    userID = payload.user_id
    user = await bot.fetch_user(userID)
    user = str(user)
    userID = '<@' + str(userID) + '>'
    user = '<' + day + '>' + str(user)
    
    if str(channel) == Channel1 or str(channel) == GENERAL:
        with open(currentFile, "r") as file:
            eventID = json.load(file)
        with open('user roles.json', "r") as file:
            userRole = json.load(file)
        try:
            eventID.remove(user)
        except Exception as e:
            print(e)

        try:
            for i in userRole:
                print(i)
                if i[0] == userID:
                    userRole.remove(i)
                    break
        except Exception as e:
            print(e)
        try:
            with open('user roles.json', "w") as file:
                json.dump(userRole, file, indent=2)
        except Exception as e:
            print(e)
        try:
            with open(currentFile, "w") as file:
                json.dump(eventID, file, indent=2)
        except Exception as e:
            print(e)
    else:
        print('REACTION REMOVED FROM WRONG CHANNEL\n')

# command '!Server' will tag all who reacted to event message
@commands.has_any_role('Admin','Owner', 'Moderator')
@bot.slash_command(guild_ids=[GUILD])
async def server(ctx):
    event = []
    eventID = []
    eventUsers = []

    try:
        with open('user roles.json', "r") as file:
            userRole = json.load(file)
    except Exception as e:
        print(e)

    try:
        with open(filename, "r") as file:
            eventID = json.load(file)
    except Exception as e:
        print(e)

    try:
        with open(currentFile, "r") as file:
            eventUsers = json.load(file)
    except Exception as e:
        print(e)

    for i in eventUsers:
        if i in event:
            pass
        else:
            eventID.append(i)
            event.append(i)

    event = []

    for user in userRole:
        if user in event:
            continue
        else:
            event.append
    channel = ctx.channel.id
    members=''
    currentMembers=[]
    xList = 0
    pList = 0
    uList = 0
    for i in userRole:
        if i[1] == 'PC' and i[0] not in currentMembers:
            pList += 1
        elif i[1] == 'XBOX' and i[0] not in currentMembers:
            xList += 1
        elif i[1] == 'UNDEF' and i[0] not in currentMembers:
            uList += 1
        if i[0] not in currentMembers:
            members= members +''+i[0]
        currentMembers.append(i[0])

    if str(channel) == GENERAL:
        embed = discord.Embed(title="Console or PC", description=f"{xList}--Xbox\n{pList}--PC\n{uList}--Unknown",color=discord.Color.gold())
        await ctx.send(embed=embed)
        await ctx.channel.send(f'{members}\n\n**Thanks For Signing up!!**')
        empty = []

        try:
            with open(filename, "w") as file:
                json.dump(eventID, file, indent=2)
        except Exception as e:
            print(e)
        try:
            with open(currentFile, "w") as file:
                json.dump(empty, file, indent=2)
        except Exception as e:
            print(e)
    else:
        print('SERVER COMMAND used in wrong channel\n')


#Sail command pings @Looking to Sail role once and then pings user who used command 3 more times to ensure they are checking the channel for updates(!dock command is used to cancel ping)
@bot.slash_command(guild_ids=[GUILD] ,description='Sail command is used to search out fellow crewmates for the seas. /n/n (/dock to cancel)')
async def sail(ctx):
    
    user = ctx.author
    channel = ctx.channel.id
    role = discord.utils.get(user.guild.roles, name='Looking to Sail')
    
       
    if str(channel) == GENERAL:
        msg = ''

        loop = 0
        while loop < 5:
            if loop == 0:
                await ctx.send(f'{user.mention} is now {role.mention}!!\n\n**(USE \'!dock\' COMMAND TO STOP RECIEVING THIS MESSAGE)**')
                try:
                    msg = await bot.wait_for('message', check=lambda message: user == ctx.author, timeout=5)
                    
                except asyncio.TimeoutError:
                    print('No user response')
                try:
                    if msg.content == '!dock':
                        await msg.delete()
                        return
                except:
                    pass
                loop += 1
            elif loop <= 3:
                await ctx.send(f'{user.mention} is still Looking for crewmates!!\n\n**(USE  "!dock" COMMAND TO STOP RECIEVING THIS MESSAGE)**')
                try:
                    msg = await bot.wait_for('message', check=lambda message: user == ctx.author, timeout=5)
                    
                except asyncio.TimeoutError:
                    print('No user response')
                try:
                    if msg.content == '!dock':
                        await msg.delete()
                        return
                except:
                    pass
                loop += 1

            else:
                await ctx.send(f'LAST CALL FOR CREWMATES!!\n\n{user.mention} is still Looking to Sail')
                loop += 1
    else:
        print('"sail" command used in wrong channel')
        
#on_message event listens for !dock command and deletes it on use. Also delete user roles.json file when message is in event channel.        
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    channel = message.channel.id
    if message.content == '!dock' and str(channel) != GENERAL:
        await message.delete()
    elif message.content == '!help':
        await message.delete()
    if str(channel) == Channel0:
        empty=[]
        try:
            with open("user roles.json", "w") as file:
                json.dump(empty, file, indent=2)
        except Exception as e:
            print(e)
        try:
            with open(currentFile, "w") as file:
                json.dump(empty, file, indent=2)
        except Exception as e:
            print(e)

    await bot.process_commands(message)

#on_command_error used to eliminate command errors on wrong command use.
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(error)

        return




#shutdown command terminates bot connection and prints message to alert user it has shutdown
@bot.slash_command(guild_ids=[GUILD], hidden=True)
async def quit(ctx):
    if str(ctx.author.id) == Creator or str(ctx.author.id) == User0:
        await ctx.send("ATTENTION: I have been murdered.")
        print('Quartermaster has been murdered by', ctx.author)
        try:
            await bot.close()
        except:
            pass
    else:
        print(f'{ctx.author} tried using QUIT command')
    
#info command displays version information and patch notes to user who called command    
@bot.slash_command(name='info', brief='Provides bot information', description='The INFO command provides detailed information about bot version and creator.')
async def info(ctx, arg=None):
    if str(ctx.author.id) == Creator or str(ctx.author.id) == User0:
        patchNotes = "Sorry Version File Not Found"
        if arg == None:
            try:
                with open(patches, "r") as file:
                    patchNotes = file.read()
            except:
                print(f'ERROR: {patches} not found!')
        else:
            versionFile = "Version" + arg + ".txt"
            try:
                with open(versionFile, "r") as file:
                    patchNotes = file.read()
            except:
                await ctx.send(f'Sorry Version {arg} Not Found')
                try:
                    with open("versions.txt", "r") as file:
                        patchNotes = file.read()
                except:
                    pass 
        embed=discord.Embed(title="Quartermaster", description=patchNotes, color=discord.Color.gold())
        await ctx.send(embed=embed)        
    
    else:
        embed=discord.Embed(title="Quartermaster", description=f"Bot version: {version}\nCreator: Reverend Studios", color=discord.Color.gold())
        await ctx.send(embed=embed)

@bot.slash_command(name='activity')
async def activity(ctx, arg=None):
    if str(ctx.author.id) == Creator or str(ctx.author.id) == User0:
        print("Admin called /Activity Command")
        attendance = []
        if arg == None:
            day = date.today()
            day = day.strftime('%m')
        else:
            day = arg
        try:
            with open(filename, "r") as file:
                attendance = json.load(file)
        except Exception as e:
            print(e)
        activeList = []
        userList = []
        msgContent = ''

        try:
            for i in attendance:
                if i in userList or day not in i:
                    continue
                else:
                    userList.append(i)

        except Exception as e:
            print(e)
        try:
            for user in userList:
                msg = [attendance.count(user), user]
                activeList.append(msg)

        except Exception as e:
            print(e)
        activeList.sort(reverse=True)
        for i in activeList:
            msgContent = msgContent + '**' + i[1] + '**' + ' = ' + str(i[0]) + '\n'
        msgContent = msgContent.replace('<', '')
        msgContent = msgContent.replace('>', '')
        msgContent = msgContent.replace(day, '')
        if msgContent == '':
            msgContent = 'None'
        try:
            await ctx.send(f"Member Activity for month of: {day} {msgContent}")
        except:
            if arg == None:
                await ctx.send(f"Sorry, No Users are recorded for the month of: {day}")
            else:
                await ctx.send(f"Sorry, No Users are recorded for the month of: {day}")
    
bot.run(TOKEN)

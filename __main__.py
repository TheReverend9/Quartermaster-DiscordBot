#!/usr/bin/env python

'''
Created on Aug 6, 2022

@author: Reverend Studios
'''
#Quartermaster bot for Sea No Evil Discord Server
#Performs multiple functions to help with the daily hassles of running a discord server.


#BOT VERSION
version = '1.0.1'
patches='Version' + version + '.txt'

import asyncio
import random
import discord
import json
import os
from dotenv import load_dotenv
from Tokens import getTokens
from datetime import date
from discord.ext.commands import bot
from discord.ext import commands
from discord.utils import get
from discord.ext.commands.core import after_invoke



#filename initialization(filename format: yyyy-mm-dd)
day = str(date.today())
filename = day + ' Server List.json'

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

#initialize lists
eventID = []
xboxList, pcList, undefinedList = [],[],[]
userIDrole = []
userRole = []


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
help_command = commands.DefaultHelpCommand(no_category = 'Commands')

bot = commands.Bot(command_prefix='!', case_insensitive=True, help_command=help_command)


# @bot.event
# async def on_ready():
    # checkTime()
    

            
            
@bot.event
async def on_raw_reaction_add(payload):
    channel = payload.channel_id
    guild = bot.get_guild(int(payload.guild_id))

    userID = payload.user_id
    
    user =  await bot.fetch_user(userID)
    # print(user)
    xboxRole = discord.utils.get(guild.roles, name='XBOX')
    pcRole = discord.utils.get(guild.roles, name='PC')
    # print(payload.member.roles)
    
    
    if str(channel) == GENERAL:
        userID = '<@' + str(userID) + '>'
        
        print()
        try:

            eventID.remove(userID)
        except:
            pass
        
        eventID.append(userID)
        
        try:
            with open(filename, "w") as file:
                json.dump(eventID, file, indent=2)
        except:
            print('FILE ERROR\n')
    

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
        
                
##on_raw_reaction_remove deletes user from list of attendees    
@bot.event
async def on_raw_reaction_remove(payload):
    loop, x = 0,0
    channel = payload.channel_id
    userID = payload.user_id
    
    
    user = await bot.fetch_user(int(payload.user_id))
    
    userID = '<@' + str(userID) + '>'
    
    
    if str(channel) == Channel1:
        if userID in eventID:
            try:
                eventID.remove(userID)
                with open(filename, "w") as file:
                    json.dump(eventID, file, indent=2)
                print('USER removed from LIST\n')
            except:
                print(f'ERROR: {filename} NOT OPENED ON REMOVE\n')
            for i in userRole:
                print(i)
                if i[0] == userID:
                    loop += 1
                    userRole.remove(i)
            try:
                with open('user roles.json', "w") as file:
                    json.dump(userRole, file, indent=2)
            except:
                print('ERROR: (user roles.json) NOT OPENED ON REMOVE\n')    
    else:
        print('REACTION REMOVED FROM WRONG CHANNEL\n')

# command '!Server' will tag all who reacted to message.
@commands.has_any_role('Admin','Owner', 'Moderator')
@bot.command(name="Server",hidden=True)
async def serverAlliance(ctx):
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

    await ctx.message.delete()
    
    if str(channel) == GENERAL:
        embed = discord.Embed(title="Console or PC", description=f"{xList}--Xbox\n{pList}--PC\n{uList}--Unknown",color=discord.Color.gold())
        await ctx.send(embed=embed)
        await ctx.channel.send(f'{members}\n\n**Thanks For Signing up!!**')
    else:
        print('SERVER COMMAND used in wrong channel\n')
        
    
    



@bot.command(name='Sail', brief='Used to find crewmates!',description='Sail command is used to search the sea\'s for crew mates. \n\nONLY AVAILABLE IN *SEA OF THE DAMNED*\n\n(USE "!dock" COMMAND TO CANCEL)')
async def lookingToSail(ctx):
    
    user = ctx.message.author
    channel = ctx.channel.id
    role = discord.utils.get(user.guild.roles, name='Looking to Sail')
    
    await ctx.message.delete() 
       
    if str(channel) == GENERAL:
        msg = ''

        loop = 0
        while loop < 5:
            if loop == 0:
                await ctx.send(f'{user.mention} is now {role.mention}!!\n\n**(USE \'!dock\' COMMAND TO STOP RECIEVING THIS MESSAGE)**')
                try:
                    msg = await bot.wait_for('message', check=lambda message: user == ctx.message.author, timeout=5)
                    
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
                    msg = await bot.wait_for('message', check=lambda message: user == ctx.message.author, timeout=5)
                    
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
            with open("user roles.json", "w") as file:
                userRole = json.load(file)
        except:
            print("ERROR: (user roles.json) Unable to be deleted.")
            
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(error)

        return




@bot.command(name='quit', hidden=True)
async def shutdown(ctx):
    if str(ctx.message.author.id) == Creator or str(ctx.message.author.id) == User0:
        await ctx.message.delete()
        await ctx.send("ATTENTION: I have been murdered.")
        print('Quartermaster has been murdered by', ctx.message.author)
        try:
            await bot.close()
        except:
            pass
    else:
        print(f'{ctx.message.author} tried using QUIT command')
    
@bot.command(name='Info', brief='Provides bot information', description='The INFO command provides detailed information about bot version and creator.')
async def info(ctx):
    if str(ctx.message.author.id) == Creator or str(ctx.message.author.id) == User0:
        try:
            with open(patches, "r") as file:
                patchNotes = file.read()
        except:
            print(f'ERROR: {patches} not found!')
        embed=discord.Embed(title="Quartermaster", description=patchNotes, color=discord.Color.gold())
        await ctx.send(embed=embed)        
    
    else:
        embed=discord.Embed(title="Quartermaster", description=f"Bot version: {version}\nCreator: Reverend Studios", color=discord.Color.gold())
        await ctx.send(embed=embed)
    await ctx.message.delete()

bot.run(TOKEN)
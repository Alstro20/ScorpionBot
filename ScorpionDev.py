import discord # Main Discord API
import asyncio #
import time
#allows import of other python scripts
from builtins import __import__
from _ast import Await
__import__
from googleapiclient.discovery import build

#import other python scripts
import key
from key import BotString, APIKey, SearchEngineID


client = discord.Client()

#[---PRE-BOOT---]
print("Starting bot")

prefix = 's!'
adminPrefix = 's@'

#List of users who are allowed to use admin commands
adminList = ['211292458208854016','194525718300983296']


def google_search(query, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
    return res['items']

#Bot comes online
@client.event
async def on_ready():
    print('Logging in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')
   
#[---COMMANDS---]
@client.event
async def on_message(message):
    if message.author != client.user: # Check to make sure the bot can't trigger its own commands
        #Command's contents are stored in commandContents
        if message.content.startswith(prefix):
            commandString = message.content
            commandContents = commandString.split(' ', 1)[-1]
            #React to the command with :scorpion:
            await client.add_reaction(message, '🦂')
        
        #Command to respond with "Pong!" (For testing)
        if message.content.startswith(prefix+'ping'):
            await client.send_message(message.channel, 'Pong!')
            #Pring "Pong!" alongside the user's username and ID
            print("Pong!", message.author, message.author.id)
            
        #Command to shut down the bot
        elif message.content.startswith(adminPrefix+'shutdown'):
            if message.author.id in adminList:
                await client.send_message(message.channel, 'Shutting down...')
                await client.change_presence(game=None,status=None,afk=False)
                time.sleep(2) # sleep for 2 seconds before shutdown, just to make sure status changed correctly
                await client.logout()
                print("Shutting down at", message.author, "'s request") 
            elif message.author.id not in adminList:
                await client.send_message(message.channel, 'Error: You are not a bot admin, '+message.author.mention)
                print(message.author, "tried to shutdown the bot but it not admin")
        
        #Command to ping the bot (again)
        elif message.content.startswith(prefix+'greet'):
            await client.send_message(message.channel, 'Hello!')
            print("Hello!", message.author)
            
        #Command to generate an invite
        elif message.content.startswith(prefix+'invite'):
            await client.send_message(message.channel, await client.create_invite(message.channel))
            print("Created server invite at", message.author, "'s request")
        
        #Command to link to a specified subreddit
        elif message.content.startswith(prefix+'reddit'):
            await client.send_message(message.channel, 'https://www.reddit.com/r/' + commandContents)
            print("Linked to subreddit", commandContents, "at", message.author, "'s request")
          
        #Command to give information about the bot  
        elif message.content.startswith(prefix+'info'):
            await client.send_message(message.author, "Scorpion bot is a little bot made by Alstro20 and EmeraldOrbis. Check out the Github project at https://github.com/Alstro20/ScorpiusStingBot")
            await client.send_message(message.channel, "Sent you a DM, " + message.author.mention)
            print("Info sent to", message.author) 
            
        #Command to make the bot say whatever
        elif message.content.startswith(prefix+'say'):
            await client.delete_message(message)
            await client.send_message(message.channel, commandContents)
            print("Said - ", commandContents, " - at the request of", message.author)
            
        #Command to make the bot google search
        elif message.content.startswith(prefix+'google'):
            resultsList = []
            print("Searched google for -", commandContents, "- at", message.author, "'s request")
            results = google_search(commandContents, APIKey, SearchEngineID, num = 3)
            for result in results:
                resultsList.append('**<' + result['link'] + '>** \n' + '```' + result['snippet'] + '```') #TODO: make this concatenation not so clunky
            await client.send_message(message.channel,  message.author.mention + ', Google search results for `' + commandContents + '`:\n'+'**1.**  '+resultsList[0]+'**2.**  '+resultsList[1]+'**3.**  '+resultsList[2])
                
        #Lets user know if script is unknown. Put all commands before this.
        elif message.content.startswith(prefix):
            await client.send_message(message.channel, 'Invalid Command')
            #Removes 🦂 emoji when invalid command
            await client.remove_reaction(message, '🦂', client.user)
            #Adds emoji when command is invalid
            await client.add_reaction(message, '⛔')

        
client.run(BotString)

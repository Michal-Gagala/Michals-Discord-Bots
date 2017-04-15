import discord
from time import sleep
from datetime import datetime
import requests
from mcstatus import MinecraftServer 
from threading import Thread # To alert for server status

cid ='287712221751148555'  # Text channel id, to get this, simply enable developer mode in discord, right click the channel and copy id
ip='xxxxx' # Server IP with the port, so: 'xxx.xxx.xxx.xxx:yyyyy'
server = MinecraftServer.lookup(ip) 
token = '' # Bot's token
client = discord.Client() # Discord client

p=True # Helper var for active server monitoring


info = """
```#mc_status gives the status of the server and time
#whoisonline gives a list of all online players```""" 

def alert(client, server, p):
    np = p
    while True:
        sleep(120) # To not kill internet connection
        try:
            p = server.ping() # If this works, server is on
        except:
            p=0 #Otherwise it has to be off

        if p:  # If there's a ping value, the connection is on
            p=True
        else:
            p=False #Otherwise it's off

        if p != np: #If status has changed, inform the user
            if not p:
                client.send_message(discord.Object(id=cid), 'Oh no, it seems the server is down!')
                print('{0} :- Alerting that server is offline'.format(datetime.now()))
            else:
                client.send_message(discord.Object(id=cid), 'YAY, it\'s back up!')
                print('{0} :- Alerting that server is back up'.format(datetime.now()))
            np = p  # Reset the 2 vars         


@client.event
async def on_message(message):
    auth = message.author
    if auth == client.user:
        return
    if message.content.startswith('#help'):
        await client.send_message(message.channel, info)
        print('{0} :- Displaying help for {1}'.format(datetime.now(), message.author))
        return
    elif message.content.startswith('#mc_status'):
        try:
            p = server.ping()
        except:
            await client.send_message(message.channel, 'Seems the server is offline!')
            print('{0} :- Server pinged, looks like it\'s offline. Request by {1}'.format(datetime.now(), message.author))
            return
        await client.send_message(message.channel, 'Server responded in {}ms'.format(p))
        print('{0} :- Displaying ping of {1} for {2}'.format(datetime.now(), p, message.author))
        return
    elif message.content.startswith('#whoisonline'):
        q = server.query()
        online = q.players.names
        no = q.players.online
        if len(online)!=0:
            await client.send_message(message.channel, '\n'.join(online))
        else:
            await client.send_message(message.channel, 'There are no online players!')            
        print('{0} :- Displaying online players, the number of which is {1}, for {2}'.format(datetime.now(), no, message.author))
        return


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    thread = Thread(target=alert, args=(client, server, p)) # Starts the active alert system
    thread.start()
client.run(token)

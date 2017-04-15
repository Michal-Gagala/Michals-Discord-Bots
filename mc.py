import discord
from time import sleep
from datetime import datetime
import requests
from mcstatus import MinecraftServer
from threading import Thread 

cid ='287712221751148555'
ip='162.244.167.111:32252'
server = MinecraftServer.lookup(ip)
token = ''
client = discord.Client()

p=True


info = """
```#mc_status gives the status of the server and time
#whoisonline gives a list of all online players```""" 

def alert(client, server, p):
    np = p
    while True:
        sleep(120)
        try:
            p = server.ping()
        except:
            p=0

        if p:
            p=True
        else:
            p=False

        if p != np:
            if not p:
                client.send_message(discord.Object(id=cid), 'Oh no, it seems the server is down!')
                print('{0} :- Alerting that server is offline'.format(datetime.now()))
            else:
                client.send_message(discord.Object(id=cid), 'YAY, it\'s back up!')
                print('{0} :- Alerting that server is back up'.format(datetime.now()))
            np = p                






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
    thread = Thread(target=alert, args=(client, server, p))
    thread.start()
client.run(token)

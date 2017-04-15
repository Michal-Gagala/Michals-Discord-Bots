import discord
from time import sleep
from datetime import datetime
from random import choice
from os import getcwd, path

cwd = getcwd()

#discord.opus.load_opus('discord')

client = discord.Client()
if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')


healz = [
    'soldier.ogg',
    'genji.ogg',
    'mccree.mp3',
    'pharah.mp3',
    'reaper.ogg',
    'sombra.ogg',
    'ana.wav',
    'dva.ogg',
    'hanzo.ogg',
    'junk.ogg',
    'lucio.ogg',
    'mei.mp3',
    'mercy.ogg',
    'rein.ogg',
    'road.ogg',
    'sym.ogg',
    'torb.ogg',
    'tracer.ogg',
    'widow.ogg'
]

japanese = [
    'mada.ogg',
    'joto.ogg',
    'sono.ogg',
    'honki.ogg',
    'mizu.ogg'
]

zen = [
    'walkinharmoony.ogg',
    'reborn.ogg',
    'universe.ogg',
    'embrace.ogg',
    'freemind.ogg',
    'gaze.ogg',
    'open.ogg',
    'walk.ogg',
    'trueself.ogg',
    'focus.ogg',
    'closedmind.ogg',
    'disciplined.ogg',
    'patient.ogg',
    'onlyvictory.ogg',
    'momentary.ogg',
    'temporary.ogg',
    'adversity.ogg',
    'outcome.ogg',
    'overconfidence.ogg',
    'pain.ogg',
    'repetition.ogg',
    'thecycle.ogg',
    'reward.ogg',
    'wadversity.ogg',
    'extinguisher.ogg'
]

info = """
*healing
*tranquility
*sights
*maths
*cheers
*sake
*mada
*jap
*freeze
*barbaric
*dblade
*dstrike
*die
*lift
*ruski
*aimbot
*molten
*bringiton
*allyouhave
*hammer
*boost
*medic
*sorry
*hi
*zen
*online
*propagando
*time
"""

sounds = {
    'healing': healz,
    'jap': japanese,
    'tranquility': ['tranquility.ogg'],
    'sights': ['sights.ogg'],
    'maths': ['maths.ogg'],
    'cheers': ['cavalry.ogg'],
    'sake': ['sake.ogg'],
    'mada': ['mada.ogg'],
    'freeze': ['freeze.ogg'],
    'barbaric': ['barbaric.ogg'],
    'dblade': ['dragonblade.ogg'],
    'dstrike': ['dragonstrike.ogg'],
    'die': ['die.ogg'],
    'lift': ['lift.ogg'],
    'ruski': ['ogon.ogg'],
    'aimbot': ['aimbot.ogg'],
    'molten': ['molten.ogg'],
    'bringiton': ['bringiton.ogg'],
    'allyouhave': ['allyouhave.ogg'],
    'hammer': ['hammer.ogg'],
    'boost': ['boost.ogg', 'speed.ogg'],
    'medic': ['medic.mp3'],
    'sorry': ['sorry.mp3'],
    'hi': ['hi.mp3'],
    'zen': zen,
    'online': ['online.ogg'],
    'propagando': ['propagando.ogg'],
    'time': ['noon.ogg']
}


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('*help'):
        await client.send_message(message.channel, info)
        print('{0} :- Displaying help for {1}'.format(datetime.now(), message.author))
        return
    for key, value in sounds.items():
        if message.content.startswith('*'+key):
            print('{0} :- Playing {1} for {2}'.format(datetime.now(), key, message.author))
            sender = message.author
            voice_channel = sender.voice.voice_channel
            voice_client = await client.join_voice_channel(voice_channel)
            if voice_client.is_connected():
                player = voice_client.create_ffmpeg_player(path.join(cwd, 'sounds', choice(value)))
                player.start()
            while not player.is_done():
                sleep(0.5)
            await voice_client.disconnect()
            return


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)

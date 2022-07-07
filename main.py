#!/usr/bin/python3

from websocket import WebSocket
from json import loads
import discord
import os
from dotenv import load_dotenv
import threading
import time
import numpy
from datetime import datetime
import markov

wsurl = "wss://steakoverflow.42paris.fr/sockjs/999/ow2ptczb/websocket"
vmsg = '["{\\"msg\\":\\"connect\\",\\"version\\":\\"1\\",\\"support\\":[\\"1\\",\\"pre2\\",\\"pre1\\"]}"]'
client = discord.Client()
channel_list = []
generator_floe = markov.create('floe.txt')
generator_lou = markov.create('lou.txt')

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content == "steakoverflow register channel":
		for stored_channel in channel_list:
			if message.channel.id == stored_channel.id:
				await message.channel.send('Error: channel already registered')
				return
		channel_list.append(message.channel)
		print(get_current_time() + " registered channel " + message.channel.name)
		await message.channel.send('Successfully registered channel')

	if message.content == "steakoverflow unregister channel":
		for stored_channel in channel_list:
			if message.channel.id == stored_channel.id:
				channel_list.remove(stored_channel) # totally not optimized but erh
				print(get_current_time() + " removed channel " + message.channel.name)
				await message.channel.send('Successfully unregistered channel')
				return
		await message.channel.send('Error: could not find channel in the database')

	if "floe" in message.content.lower():
		await message.channel.send(generator_floe.get_sentence())
	if "loulou" in message.content.lower():
		await message.channel.send('[**Lou**] ' + generator_lou.get_sentence())

	if 'florianne' in message.content.lower() and ('ça va' in message.content.lower() or 'ca va' in message.content.lower() or 'cava' in message.content.lower() or 'comment tu vas' in message.content.lower() or 'ca dit quoi' in message.content.lower()):
		if message.author.name == 'Arth':
			await message.channel.send('calme toi un peu')
		if message.author.name == 'Flosh':
			await message.channel.send('oui et toi mon croissant ?')
		if message.author.name == 'florianne':
			await message.channel.send('comment est-ce possible')
		if message.author.name == 'Eudald':
			await message.channel.send('Oui Hermano, et toi ? En Espagne il fait moins beau que sur mon balcon je suis sur')
		if message.author.name == 'louloucat':
			await message.channel.send('https://reactjs.org/docs/')
		if message.author.name == 'Azot':
			await message.channel.send('https://tenor.com/view/apmtv3-elchiringuitodejugones-elchiringuito-pedrerol-tictac-gif-22917185')
		if message.author.name == 'badria':
			await message.channel.send('non badria je ne suis pas disponible les 3 prochains mois, prend RDV\n[Badria]: **ET J\'AI UN GUN**')
		if message.author.name == 'shazam':
			await message.channel.send('oui, et toi ? tu pécho bien en Allemagne ?')
		if message.author.name == 'Sp00n':
			await message.channel.send('oui, et toi ? tu as couru combien de fois cette semaine ?')
		if message.author.name == 'lucasmln':
			await message.channel.send('Oh Lucas, cava mieux ?')
		if message.author.name == 'jmdw':
			await message.channel.send('Oui et toi Julien ? Tu as prepare ta 4eme dose ? https://www.sante.fr/cf/centres-vaccination-covid/departement-75-paris.html')
	
def get_current_time():
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	return '[' + str(current_time) + ']'

def get_food_truck_state():
	ws = WebSocket()
	ws.connect(wsurl)
	ws.recv()					# expect 'o'
	ws.send(vmsg)				# sending connect message (version etc...)
	ws.recv()					# server_id
	ws.recv()					# connected session
	truck_state = ws.recv()		# ???? food_truck state ?
	ws.close()					# don't need ws anyore
	jtruck_state = loads(loads(truck_state[1:])[0]) # double json.load
	return int(jtruck_state['fields']['history'][0]['state']) # retreive 1st state value

def notify_channels():
	print(get_current_time() + ' notifying ' + str(len(channel_list)) + ' channels')
	slots = ["12h15", "12h30", "12h45", "13h00", "13h15", "13h30", "13h45"];
	for channel in channel_list:
		print(get_current_time() + ' notifying: ' + channel.name)
		client.loop.create_task(channel.send('Le foodtruck est ouvert, ' + numpy.random.choice(slots, 1, p=[0.1, 0.2, 0.2, 0.1, 0.2, 0.1, 0.1])[0] + ' vite !!! @everyone'))

def thread_ft():
	food_truck_state = get_food_truck_state()
	while True:
		new_food_truck_state = get_food_truck_state()
		# print(new_food_truck_state)
		if new_food_truck_state != food_truck_state:
			print(get_current_time() + ' Food truck has changed state')
			food_truck_state = new_food_truck_state
			if (food_truck_state == 0): # food truck is open
				print(get_current_time() + ' Food truck is open, notifying')
				notify_channels()

		time.sleep(20)

if __name__ == "__main__":
	threading.Thread(target=thread_ft).start()
	load_dotenv()
	print(get_current_time() + ' thread started, launching bot')
	client.run(os.getenv('discord_token'))

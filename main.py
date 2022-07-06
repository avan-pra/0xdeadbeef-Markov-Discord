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

wsurl = "wss://steakoverflow.42paris.fr/sockjs/999/ow2ptczb/websocket"
vmsg = '["{\\"msg\\":\\"connect\\",\\"version\\":\\"1\\",\\"support\\":[\\"1\\",\\"pre2\\",\\"pre1\\"]}"]'
client = discord.Client()
channel_list = []

@client.event
async def on_message(message):
	if message.content == "steakoverflow register channel":
		for stored_channel in channel_list:
			if message.channel.id == stored_channel.id:
				await message.channel.send('Error: channel already registered')
				return
		channel_list.append(message.channel)
		await message.channel.send('Successfully registered channel')

	if message.content == "steakoverflow unregister channel":
		for stored_channel in channel_list:
			if message.channel.id == stored_channel.id:
				channel_list.remove(stored_channel) # totally not optimized but erh
				await message.channel.send('Successfully unregistered channel')
				return
		await message.channel.send('Error: could not find channel in the database')

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
		client.loop.create_task(channel.send('Le foodtruck est ouvert, ' + numpy.random.choice(slots, 1, p=[0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.1])[0] + ' vite !!! @everyone'))

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

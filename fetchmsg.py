#!/usr/bin/python3

'''
used to get the initial dataset for the markov chain
'''

from websocket import WebSocket
from json import loads
import discord
import os
from dotenv import load_dotenv
import threading
import time
import numpy
from datetime import datetime

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
	if (message.author == client.user or message.author.name != 'Arth' or message.content != 'fetch'):
		return

	for member in message.channel.members:
		open('db/' + member.name + '.txt', 'a').close()
	ulist = [x[:-4] + 'bot' for x in os.listdir('./db')]
	# remove .gitkeep
	ulist.pop()

	pr = await message.channel.send(get_current_time() + ' starting fetch')
	amsg = await message.channel.history(limit=100000).flatten()
	await pr.edit(content=get_current_time() + ' done fetch, parsing')
	for msg in amsg:
		# check if querying a bot

		if len(msg.content) >= 2 and 'loulou' not in msg.content and 'floe' not in msg.content and msg.content.startswith('http') == False:
			fd = open('db/' + msg.author.name + '.txt', 'a')
			fd.write(msg.content.replace('\n', ' '))
			fd.write('\n')
			fd.close()
	await pr.edit(content=get_current_time() + ' done writting dataset')
	exit()

def get_current_time():
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	return '[' + str(current_time) + ']'

if __name__ == "__main__":
	load_dotenv()
	print(get_current_time() + ' launching bot')
	client.run(os.getenv('discord_token'))

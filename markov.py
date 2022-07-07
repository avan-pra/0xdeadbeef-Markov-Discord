#!/usr/bin/python3

import sys
import numpy

class sword:
	'''contains the probablity for the starting word'''
	sword = {}
	def add(self, word):
		# we already have this word as a starting word
		if word in self.sword.keys():
			self.sword[word] += 1
		# new word
		else:
			self.sword[word] = 1

	def get(self):
		'''calculating the probability and return a word
		should be used only once per programm use so caclul are done here too'''
		w = []
		p = []
		total_possible_word = 0
		# get the total amount of 1st message (equal to the number of line in theory)
		for amount in self.sword:
			total_possible_word += self.sword[amount]
		# calculate the probability and put it in an array, useful for numpy random number 
		for word in self.sword.keys():
			w.append(word)
			p.append(self.sword[word] / total_possible_word)
		return numpy.random.choice(w, 1, p=p)[0]

	def printc(self):
		print(self.sword)

class word:
	'''contains the word, and probability for next word'''
	content = ''
	prob = {}
	p = []
	w = []
	def __init__(self, content):
		self.content = content
		self.prob = {}
		self.p = []
		self.w = []
	
	def add(self, new):
		# we already know it
		if new in self.prob.keys():
			self.prob[new] += 1
		# we don't know it
		else:
			self.prob[new] = 1

	def calculate_probabilites(self):
		'''must be called before get_next_word'''
		total_next_word = 0
		# calculate the total amount of next possible word
		for amount in self.prob:
			total_next_word += self.prob[amount]
		# calculate the probability and put it in an array, useful for numpy random number 
		for w in self.prob.keys():
			self.w.append(w)
			self.p.append(self.prob[w] / total_next_word)

	def get_next_word(self, word):
		return numpy.random.choice(self.w, 1, p=self.p)[0]

	def printc(self):
		print(self.content + ':\n    ', end='')
		for i in range(0, len(self.p)):
			if (self.w[i] == None):
				print('[' + 'None' + ' | ' + str(self.p[i]) + ']   ', end='')
			else:
				print('[' + self.w[i] + ' | ' + str(self.p[i]) + ']   ', end='')
		print()

class awords:
	'''contains all my words and manage them'''
	words = []
	s_word = None

	def __init__(self):
		words = []
		s_word = None

	def add(self, current, new):
		# loop through all know words
		for w in self.words:
			if w.content == current:
				w.add(new)
				return
		# the curren word is not known, register it
		newword = word(current)
		newword.add(new)
		self.words.append(newword)

	def calculate_probabilites(self):
		'''call calulate probabilites on all words'''
		for w in self.words:
			w.calculate_probabilites()

	def get_next_word(self, word):
		for w in self.words:
			if w.content == word:
				return w.get_next_word(word)
		return None

	def set_starting_words(self, s_word):
		self.s_word = s_word

	def get_sentence(self):
		sentence = ''
		word = self.s_word.get()
		sentence = word + ' '
		while True:
			word = self.get_next_word(word)
			if word == None:
				break
			sentence += (word + ' ')
		return sentence

	def printc(self):
		for word in self.words:
			word.printc()

def create(filename):
	a_words = awords()	# contains all word class
	s_word = sword()	# starting words

	lines = open(filename, 'r').readlines()
	# loop through all line in file
	for line in lines:
		line = line[:-1] # trim \n

		# new line, add starting word to list of starting word
		s_word.add(line.split()[0])

		# loop trough all word in the current line
		current_word = None
		sline = line.split()
		for idx, word in enumerate(sline):
			# useful not to crash
			if idx + 1 >= len(sline):
				a_words.add(word, None)
			else:
				a_words.add(word, sline[idx + 1])

	# tell all registered words to calculate probabilty to be later used for get_next_word()
	a_words.calculate_probabilites()
	# a_words.printc()
	
	a_words.set_starting_words(s_word)
	return a_words

if __name__ == "__main__":
	create()

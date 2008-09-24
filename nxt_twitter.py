#!/usr/bin/env python

import nxt.locator
import twitter
from time import sleep
import sys

class NXTtwitter():

	def __init__(self, username, password):
		self.twitter_username = username
		self.twitter_password = password
		self.nxt_mailbox = 5 # mailbox 6 on the NXT
		self.interval = 5		

	def start(self):
		alive = True
		lastcount = None
		
		while alive:
			cmd = self.get_last_message()
			if cmd and lastcount \
					and self.msgcount > lastcount:
				self.send_command(cmd)
			
			sleep(self.interval)
			lastcount = self.msgcount
		
	def connect_to_twitter(self):
		try:
			self.twitter = twitter.Api(username = self.twitter_username, 
									   password = self.twitter_password)
			print "Connected to Twitter account %s" % self.twitter_username
		except NXTtwitterError:
			raise "Can't connect to Twitter."

	def connect_to_nxt(self):
		
		try:
			nb = nxt.locator.find_one_brick()
			self.bot = nb.connect()
			print "Connected to the NXT brick.\nWaiting for commands...\n"
		except NXTtwitterError:
			self.nxt = None
			raise "Can't find or connect to NXT\nIs it turned off?"
				
	def get_last_message(self):
		messages = self.twitter.GetDirectMessages()
		self.msgcount = len(messages)
		last_message = None
		if self.msgcount > 0:
			last_message = messages[0].text.encode('ascii')
		return last_message
		
	def send_command(self, cmd):
		try:
			for i in range(2):
				self.bot.message_write(self.nxt_mailbox, cmd)
			print "%s command sent to NXT on mailbox %d." % (cmd, (self.nxt_mailbox + 1))
		except NXTtwitterError:
			raise "Can't talk to NXT.\nYou need some program running there."


class NXTtwitterError():
	pass
	
	
if __name__ == '__main__':

	if len(sys.argv) < 3:
		print "USAGE: ./nxt_twitter.py TWITTER_LOGIN TWITTER_PASSWORD"
		sys.exit(0)
	else:
		nt = NXTtwitter(sys.argv[1], sys.argv[2])
		nt.connect_to_twitter()
		nt.connect_to_nxt()
		nt.start()
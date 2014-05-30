#########################################
# Script  : Bot
# Author  : tritanbettany
# Version : 0.1
# Date    : 2014-05-24
#########################################

#Import Libraries
import socket

class Bot(object):
#
	#Class Consts
	LINE_ENDING = "\r\n"

	def __init__(self, host, port):
	#
		#Set Vars
		self.host                = host
		self.port                = port
		self.socket              = socket.socket()
		self.hostname            = socket.gethostname()
		self.connected           = 0
		self.authenticated_users = {}

		#Connect To The Network
		self.connect()	
	#

	def connect(self):
	#
		#Connect To Network
		connection_error = self.socket.connect_ex((self.host, self.port))
		if connection_error == 0:
		#
			self.connected = 1
		#

		print "New Network Connection Established To: " + self.host
	#

	def setupNick(self, nick):
	#
		#Setup Nickname
		self.nick = nick
		self.socket.send("USER " + self.nick + " 0 * :" + self.nick + self.LINE_ENDING)
		self.socket.send("NICK " + self.nick + self.LINE_ENDING)

		print "Nickname Setup as: " + self.nick
	#

	def operLogin(self, password):
	#
		#Set password used for bot admin commands
		self.bot_admin_pass = password

		#Login as Network Operator
		self.socket.send("OPER " + self.nick + " " + password + self.LINE_ENDING)
	#

	def disconnect(self):
	#
		#Disconnect From Network
		if self.checkAuth() == 1:
		#
			self.socket.send("PRIVMSG " + self.msg_from + " :\x0301,09 >> DISCONNECTING << \x03" + self.LINE_ENDING)
			self.connected = 0
			self.socket.close()

			print "Bot Disconnected By : " + self.msg_from
		#
	#

	def pingPong(self, ping_data):
	#
		#Split apart Ping Data
		pong_data = ping_data.split(":")
		pong_msg  = pong_data[1] 

		#Send PONG
		self.socket.send("PONG :" + pong_msg + self.LINE_ENDING)

		print "PONG :" + pong_msg + self.LINE_ENDING
	#

	def joinDefaultChannel(self, default_channel):
	#
		#Join the default channel
		self.default_channel = default_channel
		self.socket.send("JOIN " + self.default_channel + self.LINE_ENDING)

		print "Joined channel: " + self.default_channel

		self.requestChannelOper(self.default_channel)
	#

	def joinChannel(self, channel):
	#
		#Join a channel
		if self.checkAuth() == 1:
		#
			self.socket.send("JOIN " + channel + self.LINE_ENDING)
			self.requestChannelOper(channel)
			self.socket.send("PRIVMSG " + self.msg_from + " :\x0301,09 >> JOINED " + self.msg_args + " << \x03" + self.LINE_ENDING)

			print "Joined channel: " + channel
		#
	#

	def leaveChannel(self, channel):
	#
		#Leave a channel
		if self.checkAuth() == 1:
		#
			if channel != self.default_channel:
			#
				self.socket.send("PRIVMSG " + self.msg_from + " :\x0301,09 >> LEAVING " + self.msg_args + " << \x03" + self.LINE_ENDING)
				self.socket.send("PART " + channel + " :Tally Ho" + self.LINE_ENDING)
		
				print "Left channel: " + channel
			#
			else:
			#
				self.socket.send("PRIVMSG " + self.msg_from + " :\x0308,04 >> CANNOT LEAVE DEFAULT CHANNEL << \x03" + self.LINE_ENDING)
			#
		#
	#

	def requestChannelOper(self, channel):
	#
		#Requesting channel Oper will only work if the channel has no ops and if that command exists on the network
		self.socket.send("OPME " + channel + self.LINE_ENDING)
	
		print "Now Oper in channel: " + channel
	#

	def helloWorld(self):
	#
		#Say Hello To User
		self.socket.send("PRIVMSG " + self.msg_from + " :Hello " + self.msg_from + self.LINE_ENDING)
	#

	def help(self):
	#
		#Send help block
		self.socket.send("PRIVMSG " + self.msg_from + " :\x0311,01 >>>>> LIST OF COMMANDS <<<<< \x03" + self.LINE_ENDING)
		self.socket.send("PRIVMSG " + self.msg_from + " :\x02 >> help  \x02" + self.LINE_ENDING)
		self.socket.send("PRIVMSG " + self.msg_from + " :\x02 >> selfAuth <password>  \x02" + self.LINE_ENDING)
		self.socket.send("PRIVMSG " + self.msg_from + " :\x02 >> @killBot  \x02" + self.LINE_ENDING)
		self.socket.send("PRIVMSG " + self.msg_from + " :\x02 >> @joinChan <channel>  \x02" + self.LINE_ENDING)
		self.socket.send("PRIVMSG " + self.msg_from + " :\x02 >> @leaveChan <channel>  \x02" + self.LINE_ENDING)
		self.socket.send("PRIVMSG " + self.msg_from + " :\x1D commands with the @ symbol require you to be authorized with the bot using selfAuth  \x1D" + self.LINE_ENDING)
	#

	def sendAuthFailMessage(self):
	#
		self.socket.send("PRIVMSG " + self.msg_from + " :\x0308,04 >> AUTHORIZATION FAILED << \x03" + self.LINE_ENDING)
		print "Admin Command: " + self.msg_command + " : Failed - " + self.msg_from + " Not Authorized"
	#

	def sendAuthSuccessMessage(self):
	#
		self.socket.send("PRIVMSG " + self.msg_from + " :\x0301,09 >> AUTHORIZATION SUCCESS << \x03" + self.LINE_ENDING)
		print "Admin Command: " + self.msg_command + " : Succeeded - " + self.msg_from + " Authorized"
	#

	def setAuth(self):
	#
		#Authenticate a user to run admin commands
		if self.msg_args == self.bot_admin_pass:
		#
			self.authenticated_users[self.msg_from] = 1
			self.sendAuthSuccessMessage()

			return 1
		#
		else:
		#
			self.authenticated_users[self.msg_from] = 0
			self.sendAuthFailMessage()

			return 0
		#
	#

	def checkAuth(self):
	#
		if self.msg_from in self.authenticated_users:
		#
			if self.authenticated_users[self.msg_from] == 1:
			#
				return 1
			#
			else:
			#
				self.sendAuthFailMessage()
				return 0
			#
		#
		else:
		#
			self.sendAuthFailMessage()
			return 0
		#
	#

	def commands(self, msg_from, msg_dest, msg_content, msg_command, msg_args):
	#
		#Set Vars
		self.msg_from    = msg_from
		self.msg_dest    = msg_dest
		self.msg_content = msg_content
		self.msg_command = msg_command
		self.msg_args    = msg_args

		#Decide which command to run
		if self.msg_dest == self.nick:
		#
			#Hello World Command
			if self.msg_command == "hello" or self.msg_command == "hi" or self.msg_command == "heya" or self.msg_command == "hey" or self.msg_command == "howdy" or self.msg_command == "greetings":
			#
				self.helloWorld()
			#
			elif self.msg_command == "help":
			#
				self.help()
			#
			elif self.msg_command == "selfAuth":
			#
				self.setAuth()
			#
			elif self.msg_command == "@killBot":
			#
				self.disconnect()
			#
			elif self.msg_command == "@joinChan":
			#
				self.joinChannel(self.msg_args)
			#
			elif self.msg_command == "@leaveChan":
			#
				self.leaveChannel(self.msg_args)
			#
			else:
			#
				self.socket.send("PRIVMSG " + self.msg_from + " :I'm sorry, my responses are limited. You must ask the right questions. " + self.LINE_ENDING)
			#
		#
	#
#



















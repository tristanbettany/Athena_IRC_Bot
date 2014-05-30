#########################################
# Script  : Athena-Bot
# Author  : tritanbettany
# Version : 0.1
# Date    : 2014-05-24
#########################################

#Import Libraries
import Bot
import time

###############################################################
# Initialise Bot, Connect To The Network and Monitor In A Loop
###############################################################

athena_bot = Bot.Bot("irc.propcom.co.uk", 6667)

if athena_bot.connected == 1:
#
	athena_bot.setupNick("Athena-Bot") #This is the name of the bot
#

while athena_bot.connected == 1:
#
	#Retrive IRC message
	irc_message = athena_bot.socket.recv(2048)

	#Strip Bollocks from the IRC message
	irc_message = irc_message.strip("\r\n")

	#Handle Pings & Pongs
	if "PING :" in irc_message:
	#
		athena_bot.pingPong(irc_message)
	#

	#Join Channels Only After Message Of The Day
	if "End of /MOTD command" in irc_message:
	#
		athena_bot.operLogin("supersecretpassword") #This password is used for both bot admin commands and network operator login
		athena_bot.joinDefaultChannel("#devs") #This is the default channel for the bot
	#
	
	#Handle Real Messages from humans
	if "PRIVMSG" in irc_message:
	#
		left_right  = irc_message.split(" PRIVMSG ")
		
		#The user who sent the message
		left        = left_right[0].strip(":")
		left        = left.split("!")
		msg_from    = left[0]

		#Message Destination
		right       = left_right[1].split(" :")
		msg_dest    = right[0]

		#The actual Message
		msg_content = right[1]

		#Message commands & Arguments
		comm_args   = msg_content.split(" ")
		msg_command = comm_args[0]
		if len(comm_args) > 1:
		#
			msg_args = comm_args[1]
		#
		else:
		#
			msg_args = ''
		#

		#Decide which command to run
		athena_bot.commands(msg_from, msg_dest, msg_content, msg_command, msg_args)
	#

	#To debug Uncomment the following line and you will see the irc output in the terminal
	print irc_message
#
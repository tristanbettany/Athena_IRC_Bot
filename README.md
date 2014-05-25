Athena IRC Bot
==============

This is my first python script. It's a fairly simple IRC Bot named Athena. 

Setup
------

- Install Python
- Clone this repo or download the files **"Bot.py"** and **"athena-bot.py"** to a conveniant folder 
- Edit **"athena-bot.py"** to contain your desired, IRC network, admin password, and default channel
- Open a Terminal and change to the directory you put the files or cloned the repo
- run **"python athena-bot.py"**
- Join IRC and talk to Athena
- Add your own functions and expand Athena's abilities


Commands
---------

- **help**                   - This will show you a list of commands
- **selfAuth <password>**    - Use this to authorize yourself as an admin with the bot
- **@killBot**               - Disconnect the bot from the server and stop execution
- **@joinChan <channel>**    - Have the bot join another channel
- **@leaveChan <channel>**   - Have the bot leave a channel you joined (you can't leave the default channel)

commands with the @ symbol require you to be authorized with the bot using selfAuth

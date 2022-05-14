# SoloQ Tracker:
This is fork of script made by Aries.
The script is supposed to help coaches in League of Legends teams to keep track on how much ranked games is being played by their players.

## Changes
- Implemented LoL Pros so you don't have write puuids manually.
- Added Config.py for better clarity.
- Added separate commands, so you can decide for which time period bot will search for games.

# Installation:
1) From the Discord developer website, create an application & a bot, follow this tutorial: https://betterprogramming.pub/coding-a-discord-bot-with-python-64da9d6cade7
2) Clone this repository.
3) Once your discord bot is loaded on your Team server, here are things that you need to modify in our python script:

IN 'config.py' change the following:
- API KEY
- Discord bot token
- Player names
- Secret accounts (you can add them or delete if not needed)

## USE THE BOT:
After setting up the script, everything is pretty straight forward in terms of usage:

1) Once you made sure your API Key is refreshed, launch your python script using this command:
    `python3 bot.py`

2) After this command, you should see an outpout similar to this one:

![alt text](https://media.discordapp.net/attachments/958796003048321135/974867207106486282/unknown.png)

3) Now use following commands in server:
	1) !soloQ day - for games played in the last 24 hours.
	2) !soloQ two for games played in the last 48 hours.
	3) !soloQ week - for games played in the last week.

Have fun! ... and maybe follow me on twitter if you liked it (@dywan1na :) )
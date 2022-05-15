import discord
from discord.ext import commands, tasks
from riotwatcher import LolWatcher, ApiError
from lol_pros_accounts import LolProsAcc
from config import *
import pandas as pd
import time
import sys
from tabulate import tabulate

watcher = LolWatcher(api_key)
current_time = int(time.time())
day = 86400
week = (current_time - 604800)
two = (current_time - 172800)

def soloq(time):
    #Variables
    team_id = []
    comp_names = []
    team_mh = []
    game_nbrs = []
    L = LolProsAcc
    accounts = L.accountsByPlayers(player_name)

    #iterating over secret accounts and extending puuid list
    for secret in secret_accs:
        soloq_name = secret[1]
        comp_name = secret[0]
        puuid = watcher.summoner.by_name(my_region,soloq_name)['puuid']
        
        team_id.append(puuid)
        comp_names.append(comp_name)

    #iterating over lolpros accounts 
    for account in accounts:
        soloq_name = account[1]
        comp_name = account[0]
        puuid = watcher.summoner.by_name(my_region,soloq_name)['puuid']

        team_id.append(puuid)
        comp_names.append(comp_name)

    # Returning list of games for every player in the time period between 1 to 365
    if 90 >= int(time) > 0:
        for id in team_id:
            player_mh = []
            player_mh.extend(watcher.match.matchlist_by_puuid(region, id, queue=420, start_time=current_time-day*int(time), end_time=current_time, count=100))
            while len(player_mh) % 100 == 0 and len(player_mh) > 0:
                last_id = player_mh[-1]
                last_date = str(watcher.match.by_id(my_region,last_id)['info']['gameCreation'])[:10]
                player_mh.extend(watcher.match.matchlist_by_puuid(region, id, queue=420, start_time=current_time-day*int(time), end_time=int(last_date), count=100))
            team_mh.append(player_mh)
    else:
        return "After !soloQ there should be a number from 1 to 90"
    

    # API DATAFRAME CREATION ----------------------------------
    game_nbrs = [len(elt) for elt in team_mh]

    #prepering time string for output message
    if time == "1":
        time = "1 day."
    else:
        time = str(time) + " days."

    df = pd.DataFrame(
        {'Player': comp_names,
        'phrase': "has played",
        'Games': game_nbrs,
        'last': " games of soloQ in the last "+time,
    })

    df = df.groupby(['Player', 'phrase','last']).agg({'Games': 'sum'})
    df = df.reset_index()
    df = df[["Player","phrase","Games","last"]]
    df = df.sort_values(by=['Games'], ascending = False)
    xd = tabulate(df, showindex=False)
    print(xd)
    return xd

#DISCORD BOT COMMANDS ----------------------------------
bot = commands.Bot(command_prefix = "!", description = "SoloQ Bot")

@bot.event
async def on_ready():
	print("Your soloQ bot is ready for use !")

@bot.command()
async def soloQ(ctx, time):
    try:
        if 90 >= int(time) > 0:
            await ctx.send("https://tenor.com/view/cops-police-sirens-catching-crminals-what-you-gonna-do-gif-22472645")
            await ctx.send(soloq(time))
        else:
            return
    except:
        await ctx.send("ERROR - Try command !soloQ [number of days]")
bot.run(discord_key)
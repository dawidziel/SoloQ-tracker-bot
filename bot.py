import discord
from discord.ext import commands, tasks
import random
from riotwatcher import LolWatcher, ApiError
from lol_pros_accounts import LolProsAcc
from config import *
import pandas as pd
import csv
import time
import sys
from tabulate import tabulate

#VARIABLES
team_mh = []
game_nbrs = []
watcher = LolWatcher(api_key)
current_time = int(time.time())
day = (current_time - 86400)
week = (current_time - 604800)
two = (current_time - 172800)

def soloq(time):
    #PLAYERS
    team_id = []
    comp_names = []
    L = LolProsAcc
    accounts = L.accountsByPlayers(player_name)


    for secret in secret_accs:
        soloq_name = secret[1]
        comp_name = secret[0]
        puuid = watcher.summoner.by_name(my_region,soloq_name)['puuid']
        
        team_id.append(puuid)
        comp_names.append(comp_name)

    for account in accounts:
        soloq_name = account[1]
        comp_name = account[0]
        puuid = watcher.summoner.by_name(my_region,soloq_name)['puuid']

        team_id.append(puuid)
        comp_names.append(comp_name)

    # DAY COMMAND ----------------------------------
    if time == "day":
        team_mh = [list(watcher.match.matchlist_by_puuid(region, id, type="ranked", start_time=day, end_time=current_time, count=100)) for id in team_id]
    # WEEK COMMAND ----------------------------------
    if time == "week":
        team_mh = [list(watcher.match.matchlist_by_puuid(region, id, type="ranked", start_time=week, end_time=current_time, count=100)) for id in team_id]

    #LAST TWO DAYS COMMAND ----------------------------------
    if time == "two":
        team_mh = [list(watcher.match.matchlist_by_puuid(region, id, type="ranked", start_time=two, end_time=current_time, count=100)) for id in team_id]
    

    # API DATAFRAME CREATION ----------------------------------
    game_nbrs = [len(elt) for elt in team_mh]

    #prepering time string for output message
    if time == "two":
        last_time = "two days"
    else:
        last_time = time

    df = pd.DataFrame(
        {'Player': comp_names,
        'phrase': "has played",
        'Games': game_nbrs,
        'last': "games of soloQ in the last "+last_time+".",
    })

    df = df.groupby(['Player', 'phrase','last']).agg({'Games': 'sum'})
    df = df.reset_index()
    df = df[["Player","phrase","Games","last"]]
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
    if time == "week":
        await ctx.send("https://tenor.com/view/cops-police-sirens-catching-crminals-what-you-gonna-do-gif-22472645")
        await ctx.send(soloq("week"))
        
    elif time == "day":
        await ctx.send("https://tenor.com/view/cops-police-sirens-catching-crminals-what-you-gonna-do-gif-22472645")
        await ctx.send(soloq("day"))

    elif time == "two":
        await ctx.send("https://tenor.com/view/cops-police-sirens-catching-crminals-what-you-gonna-do-gif-22472645")
        await ctx.send(soloq("two"))
    
    else:
        return

bot.run(discord_key)
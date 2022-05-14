import json
import urllib.request

class LolProsAcc:
    def accountsByPlayers(player_names):
        accounts = []
        player_names = [x.replace(" ","-") for x in player_names]

        for playername in player_names:
            url = 'https://api.lolpros.gg/es/players/'

            with urllib.request.urlopen(url+playername) as url:
                index = json.loads(url.read().decode())

        #filtering player account (plat+) and adding it to dictionairy
            for y in index['league_player']['accounts']:
                if int(y['rank']['tier'].split("_")[0])<40:
                    accounts.append((index['name'],y['summoner_name']))
        return accounts
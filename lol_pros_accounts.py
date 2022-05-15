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

            for y in index['league_player']['accounts']:
                accounts.append((index['name'],y['summoner_name']))
                
        return accounts
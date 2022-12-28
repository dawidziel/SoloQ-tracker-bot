from mechanize import Browser
from bs4 import BeautifulSoup

class LolProsAcc:
    def accountsByPlayers(player_names):
        accounts = []
        for player_name in player_names:
            b = Browser()
            b.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
            b.open('https://lolpros.gg/player/'+player_name)
            soup = BeautifulSoup(b.response().read(), "html.parser")
            button_names = soup.find_all("button", {"class": "account"})

            if button_names != []:
                accounts.extend([(player_name, x['aria-label']) for x in button_names])
            else:
                image_name = ' '.join(soup.find("div", {"class": "summoner-name"}).text.split(' ')[:-1])
                accounts.append((player_name, image_name))
            b.close()

        return accounts

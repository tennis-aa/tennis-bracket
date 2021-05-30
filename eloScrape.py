import requests
import bs4
import os
import json
import re

# scrape elos from the tennisabstract website
page = requests.get("http://tennisabstract.com/reports/atp_elo_ratings.html")
soup = bs4.BeautifulSoup(page.text, "html.parser")
table = soup.find("table", id="reportable")
Rank = []
Player = []
Age = []
Elo = []
EloHard = []
EloClay = []
EloGrass = []
for i,row in enumerate(table.find_all('tr')):
    if i==0:
        continue
    # if i==5:
    #     break
    col = row.find_all('td')
    Rank.append(int(col[0].text))
    Player.append(col[1].text.replace("\xa0"," "))
    Age.append(float(col[2].text))
    Elo.append(float(col[3].text))
    EloHard.append(float(col[9].text))
    EloClay.append(float(col[10].text))
    EloGrass.append(float(col[11].text))


# load players.json
tournament = "Roland Garros 2021"
with open(os.path.join("docs",tournament,"players.json"),"r") as f:
    draw = json.load(f)

draw["elo"] = [1650]*len(draw["players"])
for i,p_draw in enumerate(draw["players"]):
    matches = []
    Player_indices = []
    for j,p_elo in enumerate(Player):
        x = re.search(p_draw.split()[0],p_elo)
        if x:
            matches.append(x)
            Player_indices.append(j)
    if len(matches) == 1:
        draw["elo"][i] = EloClay[Player_indices[0]]
    if len(matches) == 0:
        print("Could not find elo for",p_draw)
    if len(matches) > 1:
        print("Found more than one match for",p_draw)
    
ind = draw["players"].index("Martin")
draw["elo"][ind] = 1526
with open("players.json","w") as f:
    f.write(json.dumps(draw))
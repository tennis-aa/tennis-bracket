import requests
import bs4
import os
import json
import re
from statistics import mean, quantiles

def eloScrape(players,surface):
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


    if surface=="clay":
        EloSurface = EloClay
    elif surface=="hard":
        EloSurface = EloHard
    elif surface=="grass":
        EloSurface = EloGrass
    elif surface=="all":
        EloSurface==Elo
    else:
        raise ValueError("surface needs to be one of 'clay', 'hard', 'grass' or 'all' but surface=" + str(surface) + " is not supported.")

    elos = [1650]*len(players)
    elos_found = []
    conflicts = []
    conflicts_indices = []
    for i,p_draw in enumerate(players):
        if p_draw == "Bye":
            elos[i] = 0
            continue
        matches = []
        Player_indices = []
        for j,p_elo in enumerate(Player):
            x = re.search(p_draw.split()[1],p_elo) # the index should match the last name
            if x:
                matches.append(x)
                Player_indices.append(j)
        if len(matches) == 1:
            elos[i] = EloSurface[Player_indices[0]]
            elos_found.append(EloSurface[Player_indices[0]])
        if len(matches) == 0:
            conflicts.append(p_draw)
            conflicts_indices.append(i)
            print("Could not find elo for",p_draw)
        if len(matches) > 1:
            conflicts.append(p_draw)
            conflicts_indices.append(i)
            print("Found more than one match for",p_draw)
    
    # input for elos that were not found
    quartiles = quantiles(elos_found,n=4)
    print("Elo stats: min=",min(elos_found),"; Q1=",quartiles[0],"; median=",quartiles[1],"; avg=",mean(elos_found),"; Q3=",quartiles[2],"; max=",max(elos_found))
    manually = input("Do you want to input missing Elo ratings manually? (if not, missing elo ratings are imputed with the median) [y/n]: ")
    for i in range(len(conflicts)):
        if manually == "y":
            elo = input("Enter Elo rating for " + conflicts[i] + ": ")
            elos[conflicts_indices[i]] = float(elo)
        else:
            elos[conflicts_indices[i]] = quartiles[1]

    return elos

if __name__=="__main__":
    eloScrape(["N Djokovic","R Federer"])
'''
This function creates a new folder for a new tournament
'''

import os
import jinja2
import sys
import math
import json
import traceback
from . import playerScrape
from . import eloScrape
from . import basicBrackets

def bracketRender(tournament,atplink,bracketSize,path=None,surface="all",points_per_round=[1,2,3,5,7,10,15],cellheight=16,vspace=32,hspace=90,linewidth=1):
    # Parameters for creating the tournament folder
    # tournament = "RGtest"
    # surface = "clay" # "all", "hard", "clay", or "grass" used for scraping the elos
    # atplink = "https://www.atptour.com/en/scores/current/roland-garros/520/draws"
    # bracketSize = 128
    # points_per_round = [1,2,3,5,7,10,15]

    # # Parameters for appearance of the bracket
    # cellheight = 16 #pixels
    # vspace = 2*cellheight
    # hspace = 90 #pixels
    # linewidth = 1 #pixels

    rounds = math.log(bracketSize,2)
    if not rounds.is_integer():
            raise ValueError("bracketSize has to be 2^n")
    rounds = int(rounds)

    # input variables
    counter = [0]*(rounds+1)
    for j in range(rounds):
        counter[j+1] = counter[j] + int(bracketSize/(2**j))
    # print(counter)

    render_vars = {"bracketSize" : bracketSize, "rounds" : rounds, "counter" : counter, "tournament": tournament,
    "cellheight": cellheight, "vspace": vspace, "hspace": hspace, "linewidth": linewidth}

    
    script_path = os.getcwd()
    if path is None:
        target_file_path = os.path.join(script_path, "docs" , tournament)
    else:
        target_file_path = os.path.join(path,tournament)

    if not os.path.exists(target_file_path):
        os.mkdir(target_file_path)

    # Display bracket
    template_filename = "./templateBracketDisplay.jinja"
    fileName="index.html"
    rendered_file_path = os.path.join(target_file_path, fileName)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))
    environment.trim_blocks = True
    environment.lstrip_blocks = True
    output_text = environment.get_template(template_filename).render(render_vars)
    with open(rendered_file_path, "w") as result_file:
        result_file.write(output_text)

    # Fillout bracket
    template_filename = "./templateBracketFillout.jinja"
    fileName="submit.html"
    rendered_file_path = os.path.join(target_file_path, fileName)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))
    environment.trim_blocks = True
    environment.lstrip_blocks = True
    output_text = environment.get_template(template_filename).render(render_vars)
    with open(rendered_file_path, "w") as result_file:
        result_file.write(output_text)

    # table of positions
    template_filename = "./templateTablePositions.jinja"
    fileName="table.html"
    rendered_file_path = os.path.join(target_file_path, fileName)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))
    environment.trim_blocks = True
    environment.lstrip_blocks = True
    output_text = environment.get_template(template_filename).render(render_vars)
    with open(rendered_file_path, "w") as result_file:
        result_file.write(output_text)

    # Results bracket
    template_filename = "./templateBracketResults.jinja"
    fileName="inputResults.html"
    rendered_file_path = os.path.join(target_file_path, fileName)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))
    environment.trim_blocks = True
    environment.lstrip_blocks = True
    output_text = environment.get_template(template_filename).render(render_vars)
    with open(rendered_file_path, "w") as result_file:
        result_file.write(output_text)

    # json files
    with open(os.path.join(target_file_path, "config.json"),"w") as f:
        f.write(json.dumps({"tournament":tournament,"points_per_round": points_per_round,"atplink":atplink,"bracketSize":bracketSize,"surface":surface},indent=4))
    
    
    if not os.path.exists(os.path.join(target_file_path,"players.json")):
        try:
            ATPData = playerScrape.ATPdrawScrape(atplink)
            elos = eloScrape.eloScrape(ATPData["players"],surface)

            with open(os.path.join(target_file_path, "players.json"),"w") as f:
                f.write(json.dumps({"players": ATPData["players"], "elo": elos}))

            # Create monkeys, bots, and Elo brakets
            monkeys = basicBrackets.generateMonkeys(ATPData["players"], 10000)
            bots = basicBrackets.generateBots(ATPData["players"], elos, 10000)
            Elo = basicBrackets.generateElo(ATPData["players"], elos)

            with open(os.path.join(target_file_path, "Elo.json"),"w") as f:
                f.write(json.dumps(Elo))
        except:
            traceback.print_exc()
            print("The players and Elo ratings could not be downloaded. You need to fill out players.json manually")
            with open(os.path.join(target_file_path, "players.json"),"w") as f:
                f.write(json.dumps({"players": [""]*bracketSize, "elo": [1500]*bracketSize}))

    return



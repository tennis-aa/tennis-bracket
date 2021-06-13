'''
This script creates a new folder for a new tournament
The parameters at the beginning of function bracketrender contain
the information of the tournament (name and draw size)
'''

import os
import jinja2
import sys
import math
import json
import traceback
import playerScrape
import eloScrape
import basicBrackets

def bracketRender():
    # Parameters for creating the tournament folder
    tournament = "RGtest"
    surface = "clay" # "all", "hard", "clay", or "grass" used for scraping the elos
    atplink = "https://www.atptour.com/en/scores/current/roland-garros/520/draws"
    bracketSize = 128
    points_per_round = [1,2,3,5,7,10,15]

    # Parameters for appearance of the bracket
    cellheight = 16 #pixels
    vspace = 2*cellheight
    hspace = 90 #pixels
    linewidth = 1 #pixels
    # Do not change anything below here

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

    script_path = os.path.dirname(os.path.abspath(__file__))
    target_file_path = os.path.join(script_path, "docs" , tournament)
    if not os.path.exists(target_file_path):
        os.mkdir(target_file_path)
    
    # config.json file
    with open(os.path.join(target_file_path, "config.json"),"w") as f:
        f.write(json.dumps({"tournament":tournament,"points_per_round": points_per_round,"atplink":atplink,"bracketSize":bracketSize,"surface":surface},indent=4))
    with open(os.path.join(target_file_path, "players.json"),"w") as f:
        f.write(json.dumps({"players": [""]*bracketSize, "elo": [1650]*bracketSize}))
    with open(os.path.join(target_file_path, "results.json"),"w") as f:
        f.write(json.dumps({"results": [""]*(bracketSize-1), "scores": [""]*(bracketSize-1), "losers": [], "table_results": {"user": [],"points":[],"potential":[],"position":[],"rank":[],"monkey_rank":[],"bot_rank":[]}}))
    with open(os.path.join(target_file_path, "brackets.json"),"w") as f:
        f.write(json.dumps({}))
    with open(os.path.join(target_file_path, "monkeys.json"),"w") as f:
        f.write(json.dumps({}))
    with open(os.path.join(target_file_path, "bots.json"),"w") as f:
        f.write(json.dumps({}))


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


    try:
        ATPData = playerScrape.ATPdrawScrape(atplink)
        elos = eloScrape.eloScrape(ATPData["players"],surface)

        with open(os.path.join(target_file_path, "players.json"),"w") as f:
            f.write(json.dumps({"players": ATPData["players"], "elo": elos}))

        # Create monkeys, bots, and Elo brakets
        monkeys = basicBrackets.generateMonkeys(ATPData["players"], 10000)
        bots = basicBrackets.generateBots(ATPData["players"], elos, 10000)
        Elo = basicBrackets.generateElo(ATPData["players"], elos)

        with open(os.path.join(target_file_path, "monkeys.json"),"w") as f:
            f.write(json.dumps(monkeys))
        with open(os.path.join(target_file_path, "bots.json"),"w") as f:
            f.write(json.dumps(bots))
        with open(os.path.join(target_file_path, "Elo.json"),"w") as f:
            f.write(json.dumps(Elo))
    except:
        traceback.print_exc()
        print("The players and Elo ratings could not be loaded from the website. You need to fill out players.json, monkeys.json, bots.json, and Elo.json")
        


if __name__ == "__main__":
    bracketRender()


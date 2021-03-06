import pybracket

tournament = "Paris 2021" 
atplink = "https://www.atptour.com/en/scores/current/paris/352/draws" # link to ATP website to scrape players
bracketSize = 64 # Number of players 128, 64, 32 (if there are byes in the tournament inlude them in the bracketSize, i.e., do not enter 48 or 24)
path = None # By default the files will be saved to /docs/tournament, but you can choose another path
surface = "hard" # all, hard, clay, or grass. This is used to obtain the Elo rating of the players. "all" is the default for overall Elo rating
points_per_round = [1,2,3,5,7,10,15] # The number of points competitors receive for a correct pick in each round
sets = 3 # 3 for best of three sets matches and 5 for best of five sets matches
# You can control the appearance of the bracket by specifying the cellheight, vspace, hspace, and linewidth in pixels 

pybracket.bracketRender(tournament, atplink, bracketSize, path, surface, points_per_round,sets)

# Remember to add the tournament link to the home page
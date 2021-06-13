import os
import math
import json
import playerScrape
import eloScrape
import basicBrackets

class Bracket:
    def __init__(self,players=[],elo=[],results=[],scores=[],losers=[],table_results={"user": [],"points":[],"potential":[],"position":[],"rank":[],"monkey_rank":[],"bot_rank":[]},brackets={},monkeys={},bots={},tournament="",path="",points_per_round=[1,2,3,5,7,10,15],atplink="",surface="all"):
        self.players = players
        self.bracketSize = len(players)
        self.elo = elo
        self.results = results
        self.scores = scores
        self.losers = losers
        self.table_results = table_results
        if self.bracketSize == 0:
            self.rounds = 0
        else:
            self.rounds = int(math.log2(self.bracketSize))
        self.brackets = brackets
        self.monkeys = monkeys
        self.bots = bots
        self.tournament = tournament
        self.path = path
        self.points_per_round = points_per_round
        self.atplink = atplink
        self.surface = surface
        self.counter = [0]*(self.rounds+1)
        for j in range(self.rounds):
            self.counter[j+1] = self.counter[j] + int(self.bracketSize/(2**j))
    
    def loadFromFolder(self,path=None):
        if path is not None:
            self.path = path

        with open(os.path.join(self.path, "config.json"),"r") as f:
            config = json.load(f)
        self.tournament = config["tournament"]
        self.points_per_round = config["points_per_round"]
        self.atplink = config["atplink"]
        self.bracketSize = config["bracketSize"]
        if self.bracketSize == 0:
            self.rounds = 0
        else:
            self.rounds = int(math.log2(self.bracketSize))
        self.counter = [0]*(self.rounds+1)
        for j in range(self.rounds):
            self.counter[j+1] = self.counter[j] + int(self.bracketSize/(2**j))
        self.surface = config["surface"]
        with open(os.path.join(self.path, "players.json"),"r") as f:
            players_json = json.load(f)
        self.players = players_json["players"]
        self.elo = players_json["elo"]
        if len(self.players) != self.bracketSize:
            print("Warning: the number of players and the bracketSize do not match.")

        with open(os.path.join(self.path, "brackets.json"),"r") as f:
            self.brackets = json.load(f)

        with open(os.path.join(self.path, "monkeys.json"),"r") as f:
            self.monkeys = json.load(f)
        with open(os.path.join(self.path, "bots.json"),"r") as f:
            self.bots = json.load(f)
        with open(os.path.join(self.path, "results.json"),"r") as f:
            results_json = json.load(f)
        self.results = results_json["results"]
        self.scores = results_json["scores"]
        self.losers = results_json["losers"]
        self.table_results = results_json["table_results"]

    def computePoints(self,bracket):
        if len(bracket) != (self.bracketSize - 1):
            raise ValueError("The bracket is not the correct length> The correct is " + str(self.bracketSize-1))
        points = 0
        rd = 0
        for i in range(len(bracket)):
            if i+self.bracketSize >= self.counter[rd+2]:
                rd = rd+1
            if bracket[i] == self.results[i] and self.results[i] != "":
                points = points + self.points_per_round[rd]

        # deduct points from byes
        for i in range(len(self.players)):
            if self.players[i] == "Bye":
                points = self.points-points_per_round[0]
        
        return points

    def computePotential(self,bracket):
        if len(bracket) != self.bracketSize - 1:
            raise ValueError("The bracket is not the correct length> The correct is " + str(self.bracketSize-1))
        potential = 0
        rd = 0
        for i in range(len(bracket)):
            if i+self.bracketSize >= self.counter[rd+2]:
                rd = rd + 1
            if bracket[i] == "":
                continue
            if self.results[i] == bracket[i]:
                potential = potential + self.points_per_round[rd]
            elif self.results[i]=="" and not (bracket[i] in self.losers):
                potential = potential + self.points_per_round[rd]
            
        for i in range(len(self.players)):
            if self.players[i] == "Bye":
                potential = potential-self.points_per_round[0]

        return potential

    def updatePlayers(self):
        ATPData = playerScrape.ATPdrawScrape(self.atplink) # players, results, scores
        players = ATPData["players"]
        conflicts_old = []
        conflicts_new = []
        for i in range(len(self.players)):
            if self.players[i] != players[i]:
                conflicts_old.append(self.players[i]) 
                conflicts_new.append(players[i])

        # method to update changes to the draw
        if len(conflicts_old)>0:
            print("The following conflicts were found:")
            print(json.dumps({conflicts_old[i]:conflicts_new[i] for i in range(len(conflicts_old))},indent=4))
            change = input("Do you want to update the players? [y/n]: ")
            if change != "y":
                raise Exception("You will not be able to update results if there are conflicts between the bracket files and the ATP website.")
            
            # players.json
            self.players = players
            
            # brackets.json
            for key in self.brackets:
                self.brackets[key] = playerUpdate(self.brackets[key], conflicts_old, conflicts_new)

            # monkeys.json
            for key in self.monkeys:
                self.monkeys[key] = playerUpdate(self.monkeys[key], conflicts_old, conflicts_new)

            # bots.json
            for key in self.bots:
                self.bots[key] = playerUpdate(self.bots[key], conflicts_old, conflicts_new)
            
            print("You can run method Bracket.updateElo() to update the elo ratings and Bracket.updateBots() to update the bot brackets with the updated Elo ratings.")
        
        return
    
    def updateElo(self):
        elos = eloScrape.eloScrape(self.players,self.surface)
        self.elo = elos
        return

    def updateBots(self,n=10000):
        self.bots = basicBrackets.generateBots(self.players, self.elo, n)
        return

    def updateMonkeys(self,n=10000):
        self.monkeys = basicBrackets.generateMonkeys(self.players, n)

    def updateBrackets(self,user,bracket):
        self.brackets[user] = bracket
        return

    def updateResults(self):
        ATPData = playerScrape.ATPdrawScrape(self.atplink) # players, results, scores
        players = ATPData["players"]
        results = ATPData["results"]
        scores = ATPData["scores"]

        for i in range(len(self.players)):
            if self.players[i] != players[i]:
                raise Exception("There is a conflict betwen the players found on the ATP website and the bracket files. Run the Bracket.updatePlayers() method to resolve conflicts.")

        self.results = results
        self.scores = scores

        losers = []
        for i in range(int(self.bracketSize/2)):
            if results[i] != "":
                if results[i] == players[2*i] and players[2*i+1] != "Bye":
                    losers.append(players[2*i+1])
                elif results[i] == players[2*i+1] and players[2*i] != "Bye":
                    losers.append(players[2*i])
        
        for j in range(2,self.rounds+1):
            for i in range(int(self.bracketSize/(2**j))):
                if results[self.counter[j]+i-self.bracketSize] != "":
                    if results[self.counter[j]+i-self.bracketSize] == results[self.counter[j-1]+2*i-self.bracketSize]:
                        losers.append(results[self.counter[j-1]+2*i+1-self.bracketSize])
                    elif (results[self.counter[j]+i-self.bracketSize] == results[self.counter[j-1]+2*i+1-self.bracketSize]):
                        losers.append(results[self.counter[j-1]+2*i-self.bracketSize])
        self.losers = losers

        # Define the object that contains the standings
        table_results = {"user": [],"points":[],"potential":[],"position":[],"rank":[],"monkey_rank":[],"bot_rank":[]}
        # compute points and positions for all participants
        entries = []
        for key in self.brackets:
            points = self.computePoints(self.brackets[key])
            entries.append({"user":key,"points":points,"position":1,"rank":""})
        entries.sort(key=lambda x:x["points"],reverse=True)
        nr_users = len(entries)
        for i in range(1,nr_users):
            if entries[i]["points"] == entries[i-1]["points"]:
                entries[i]["position"] = entries[i-1]["position"]
            else:
                entries[i]["position"] = i+1

        # compute rank
        for i in range(nr_users):
            if entries[i]["position"] <= math.ceil(nr_users/2):
                entries[i]["rank"] = "top " + str(round((entries[i]["position"]-1/2)/nr_users*100)) + "%"
            else:
                entries[i]["rank"] = "bot " + str(round((nr_users-entries[i]["position"]+1/2)/nr_users*100)) + "%"
            table_results["user"].append(entries[i]["user"])
            table_results["points"].append(entries[i]["points"])
            table_results["position"].append(entries[i]["position"])
            table_results["rank"].append(entries[i]["rank"])

        # compute potential points
        for i in range(nr_users):
            potential = self.computePotential(self.brackets[table_results["user"][i]])
            table_results["potential"].append(potential)

        # compute rank among monkeys
        monkey_points = []
        for key in self.monkeys:
            monkey_points.append(self.computePoints(self.monkeys[key]))

        monkey_points.sort(reverse=True)
        for i in range(nr_users):
            if table_results["points"][i] < monkey_points[-1]:
                table_results["monkey_rank"].append(100)
                continue
            for j in range(len(monkey_points)):
                if table_results["points"][i] >= monkey_points[j]:
                    table_results["monkey_rank"].append(round(j/len(monkey_points)*100))
                    break

        # compute rank among bots
        bot_points = []
        for key in self.bots:
            bot_points.append(self.computePoints(self.bots[key]))

        bot_points.sort(reverse=True)
        for i in range(nr_users):
            if table_results["points"][i] < bot_points[-1]:
                table_results["bot_rank"].append(100)
                continue
            for j in range(len(bot_points)):
                if table_results["points"][i] >= bot_points[j]:
                    table_results["bot_rank"].append(round(j/len(bot_points)*100))
                    break

        self.table_results = table_results
        return


    def save(self):
        with open(os.path.join(self.path, "config.json"),"w") as f:
            f.write(json.dumps({"tournament":self.tournament,"points_per_round": self.points_per_round,"atplink":self.atplink,"bracketSize":self.bracketSize,"surface":self.surface},indent=4))
        with open(os.path.join(self.path, "players.json"),"w") as f:
            f.write(json.dumps({"players": self.players, "elo": self.elo}))
        with open(os.path.join(self.path, "brackets.json"),"w") as f:
            f.write(json.dumps(self.brackets))
        with open(os.path.join(self.path, "results.json"),"w") as f:
            f.write(json.dumps({"results":self.results,"scores":self.scores,"losers":self.losers,"table_results":self.table_results}))
        with open(os.path.join(self.path, "monkeys.json"),"w") as f:
            f.write(json.dumps(self.monkeys))
        with open(os.path.join(self.path, "bots.json"),"w") as f:
            f.write(json.dumps(self.bots))
        

# END OF CLASS


def playerUpdate(player_list,players_old,players_new):

    if len(players_old) != len(players_new):
        raise ValueError("The list of old and new players has to be the same length.")

    # First replace all conflicts with another string to avoid double replacing players that were just moved in the draw
    for i,pl in enumerate(players_old):
        player_list = ["NEWPLAYER"+str(i) if j == pl else j for j in player_list]

    # Now replace with the new player
    for i,pl in enumerate(players_new):
        player_list = [pl if j == "NEWPLAYER"+str(i) else j for j in player_list]

    return player_list
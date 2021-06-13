from bracketClass import Bracket

bracket1 = Bracket(path="docs/RGtest")
bracket1.loadFromFolder()

bracket2 = Bracket()
bracket2.loadFromFolder(path="docs/RGtest")

bracket1.players == bracket2.players

bracket1.results

bracket1.players[0] = "pepito"
bracket1.players
bracket1.updateResults()
bracket1.updatePlayers()

bracket1.updateElo()

bracket1.updateResults()
bracket1.results
bracket1.scores
bracket1.losers
bracket1.table_results

bracket1.updateBots()
bracket1.bots["bot1"]
bracket2.bots["bot1"]

bracket1.updateMonkeys()

bracket1.save()
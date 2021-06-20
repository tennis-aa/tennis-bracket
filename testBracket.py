from pybracket import Bracket

bracket1 = Bracket(path="docs/Roland Garros 2021")
bracket1.loadFromFolder()

bracket2 = Bracket()
bracket2.loadFromFolder("docs/Roland Garros 2021")
bracket2.loadFromFolder(path="docs/Roland Garros 2021")

bracket1 == bracket2
bracket1.players == bracket2.players

bracket1.results

bracket1.players[0] = "pepito"
bracket1.players
bracket1.updateResults(scrape=False)
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

bracket1.updateMonkeys(3)

bracket1.save()
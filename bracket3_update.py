import pybracket

tournament = "Wimbledon 2021"
path = "docs/" + tournament
b = pybracket.Bracket()
b.loadFromFolder(path)

# If there are changes to the draw before the tournament starts (e.g., withdrawals) the following commands may be useful
# b.updatePlayers()
# b.updateElo("Y Uchiyama (LL)",1446.0)
# b.updateElobracket()

b.updateResults(scrape=True)
b.save()
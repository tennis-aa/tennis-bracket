import pybracket

tournament = "Paris 2021"
path = "docs/" + tournament
b = pybracket.Bracket()
b.loadFromFolder(path)

# If there were qualifier placeholders when the brackets were filled out, the following commands are useful
# b.updatePlayers()
# b.updateElo()
# b.updateElobracket()

# If there are changes to the draw before the tournament starts (e.g., withdrawals) the following commands may be useful
# b.updatePlayers()
# b.updateElo("Y Sugita",1526)
# b.updateElobracket()

b.updateResults(scrape=True)
b.save()